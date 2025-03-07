# network_monitor.py - Network packet monitoring for honeypot

import scapy.all as scapy
from datetime import datetime
import os
from config import PORTS
from logger import log_packet  # Use logger.py for consistency

HONEYPOT_PORTS = set(PORTS.values())

def packet_callback(packet, shutdown_event=None):
    if packet.haslayer(scapy.IP):
        src_ip = packet[scapy.IP].src
        dst_ip = packet[scapy.IP].dst
        protocol = packet[scapy.IP].proto
        src_port = packet[scapy.TCP].sport if packet.haslayer(scapy.TCP) else None
        dst_port = packet[scapy.TCP].dport if packet.haslayer(scapy.TCP) else None
        if src_port in HONEYPOT_PORTS or dst_port in HONEYPOT_PORTS:
            service = port_to_service(dst_port) or port_to_service(src_port) or "Unknown"
            log_packet(service, src_ip, {
                "destination_ip": dst_ip,
                "protocol": protocol_name(protocol),
                "source_port": src_port,
                "destination_port": dst_port,
                "length": len(packet)
            })
            print(f"[NETWORK] Packet captured - {src_ip}:{src_port} -> {dst_ip}:{dst_port}")

def protocol_name(proto_num):
    """Convert protocol number to name."""
    return {1: "ICMP", 6: "TCP", 17: "UDP"}.get(proto_num, f"Unknown ({proto_num})")

def port_to_service(port):
    """Map port to service name."""
    return {2222: "SSH", 8080: "HTTP", 2121: "FTP"}.get(port)

def start_packet_sniffing(shutdown_event=None):
    """Start sniffing packets, stopping on shutdown event."""
    print("[NETWORK] Starting packet sniffing...")
    try:
        # Check for admin privileges (Unix-like systems)
        if os.name == "posix" and os.geteuid() != 0:
            raise PermissionError("Packet sniffing requires root privileges. Run with sudo.")
        
        # BPF filter for honeypot ports
        bpf_filter = "ip and (" + " or ".join(f"port {port}" for port in HONEYPOT_PORTS) + ")"
        print(f"[NETWORK] Filter: {bpf_filter}")

        # Sniff with stop condition
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

if __name__ == "__main__":
    # For standalone testing
    from threading import Event
    shutdown_event = Event()
    start_packet_sniffing(shutdown_event)