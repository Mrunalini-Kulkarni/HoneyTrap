# fake_services/fake_http.py - Fake HTTP Honeypot Service

import socket
import threading
from logger import log_packet as log_attack  # Alias for consistency
from config import PORTS, FAKE_BANNERS

def handle_http_connection(client_socket):
    try:
        client_ip = client_socket.getpeername()[0]
        banner = FAKE_BANNERS["HTTP"].encode()
        client_socket.send(banner)
        log_attack("HTTP", client_ip, {"length": len(banner)})  # Log sent banner size
    except Exception as e:
        print(f"[HTTP] Error handling connection from {client_ip}: {e}")
    finally:
        client_socket.close()

def start_http_honeypot():
    """
    Starts the fake HTTP honeypot on the configured port.
    """
    http_port = PORTS["HTTP"]
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", http_port))
    server_socket.listen(5)

    print(f"[HTTP] Honeypot listening on port {http_port}...")

    while True:
        client_socket, _ = server_socket.accept()
        thread = threading.Thread(target=handle_http_connection, args=(client_socket,))
        thread.start()
