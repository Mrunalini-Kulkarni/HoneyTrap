# network_monitor.py - Network packet monitoring for honeypot

import scapy.all as scapy
from datetime import datetime
import os
from config import PORTS
from logger import log_packet

HONEYPOT_PORTS = set(PORTS.values())

# Trie for payload pattern matching
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
        for pattern in ["exploit", "shellcode", "login"]:
            self.insert(pattern)

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def search(self, text):
        node = self.root
        for i, char in enumerate(text):
            if char in node.children:
                node = node.children[char]
                if node.is_end:
                    return text[max(0, i - 8):i + 1]  # Extract context
        return None

pattern_trie = Trie()

def packet_callback(packet, shutdown_event=None):
    if packet.haslayer(scapy.IP):
        src_ip = packet[scapy.IP].src
        dst_ip = packet[scapy.IP].dst
        src_port = packet[scapy.TCP].sport if packet.haslayer(scapy.TCP) else None
        dst_port = packet[scapy.TCP].dport if packet.haslayer(scapy.TCP) else None
        if src_port in HONEYPOT_PORTS or dst_port in HONEYPOT_PORTS:
            service = port_to_service(dst_port) or port_to_service(src_port) or "Unknown"
            info = {
                "destination_ip": dst_ip,
                "protocol": protocol_name(packet[scapy.IP].proto),
                "source_port": src_port,
                "destination_port": dst_port,
                "length": len(packet)
            }
            if packet.haslayer(scapy.Raw):
                payload = packet[scapy.Raw].load.decode(errors="ignore")
                match = pattern_trie.search(payload)
                if match:
                    info["pattern"] = match
            log_packet(service, src_ip, info)
            print(f"[NETWORK] Packet captured - {src_ip}:{src_port} -> {dst_ip}:{dst_port}")

def protocol_name(proto_num):
    return {1: "ICMP", 6: "TCP", 17: "UDP"}.get(proto_num, f"Unknown ({proto_num})")

def port_to_service(port):
    return {2222: "SSH", 8080: "HTTP", 2121: "FTP"}.get(port)

def start_packet_sniffing(shutdown_event=None):
    print("[NETWORK] Starting packet sniffing...")
    try:
        if os.name == "posix" and os.geteuid() != 0:
            raise PermissionError("Packet sniffing requires root privileges. Run with sudo.")
        bpf_filter = "ip and (" + " or ".join(f"port {port}" for port in HONEYPOT_PORTS) + ")"
        print(f"[NETWORK] Filter: {bpf_filter}")
        scapy.sniff(
            prn=lambda pkt: packet_callback(pkt, shutdown_event),
            store=False,
            filter=bpf_filter,
            stop_filter=lambda _: shutdown_event.is_set() if shutdown_event else False
        )
    except PermissionError as e:
        print(f"[NETWORK ERROR] {str(e)}")
    except Exception as e:
        print(f"[NETWORK ERROR] Failed to start sniffing: {str(e)}")
    finally:
        print("[NETWORK] Packet sniffing stopped.")