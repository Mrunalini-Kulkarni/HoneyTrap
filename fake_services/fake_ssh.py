# fake_services/fake_ssh.py - Fake SSH Honeypot Service

import socket
import threading
from logger import log_packet as log_attack
from config import PORTS, FAKE_BANNERS

def handle_ssh_connection(client_socket):
    try:
        client_ip, _ = client_socket.getpeername()
        server_ip, server_port = client_socket.getsockname()  # Get server IP
        client_socket.send(FAKE_BANNERS["SSH"].encode())
        data = client_socket.recv(1024).decode(errors="ignore")
        log_attack("SSH", client_ip, {"input": data, "length": len(data), "destination_ip": server_ip})
        if "user" in data.lower():
            client_socket.send(b"Password: ")
            password = client_socket.recv(1024).decode(errors="ignore")
            log_attack("SSH", client_ip, {"password_attempt": password, "destination_ip": server_ip})
    except Exception as e:
        print(f"[SSH] Error handling connection from {client_ip}: {e}")
    finally:
        client_socket.close()

def start_ssh_honeypot():
    ssh_port = PORTS["SSH"]
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server_socket.bind(("0.0.0.0", ssh_port))
        server_socket.listen(5)
        print(f"[SSH] Honeypot listening on port {ssh_port}...")
        while True:
            client_socket, _ = server_socket.accept()
            thread = threading.Thread(target=handle_ssh_connection, args=(client_socket,))
            thread.start()
    except Exception as e:
        print(f"[SSH] Failed to start: {e}")