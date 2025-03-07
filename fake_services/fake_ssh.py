# fake_services/fake_ssh.py - Fake SSH Honeypot Service

import socket
import threading
from logger import log_packet as log_attack  # Alias for consistency
from config import PORTS, FAKE_BANNERS

def handle_ssh_connection(client_socket):
    try:
        client_ip = client_socket.getpeername()[0]
        banner = FAKE_BANNERS["SSH"].encode()
        client_socket.send(banner)
        log_attack("SSH", client_ip, {"length": len(banner)})  # Log sent banner size
    except Exception as e:
        print(f"[SSH] Error handling connection from {client_ip}: {e}")
    finally:
        client_socket.close()

def start_ssh_honeypot():
    """
    Starts the fake SSH honeypot on the configured port.
    """
    ssh_port = PORTS["SSH"]
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", ssh_port))
    server_socket.listen(5)

    print(f"[SSH] Honeypot listening on port {ssh_port}...")

    while True:
        client_socket, _ = server_socket.accept()
        thread = threading.Thread(target=handle_ssh_connection, args=(client_socket,))
        thread.start()
