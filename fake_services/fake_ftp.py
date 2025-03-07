# fake_services/fake_ftp.py - Fake FTP Honeypot Service

import socket
import threading
from logger import log_packet as log_attack  # Alias for consistency
from config import PORTS, FAKE_BANNERS

def handle_ftp_connection(client_socket):
    try:
        client_ip = client_socket.getpeername()[0]
        banner = FAKE_BANNERS["FTP"].encode()
        client_socket.send(banner)
        log_attack("FTP", client_ip, {"length": len(banner)})  # Log sent banner size
    except Exception as e:
        print(f"[FTP] Error handling connection from {client_ip}: {e}")
    finally:
        client_socket.close()

def start_ftp_honeypot():
    """
    Starts the fake FTP honeypot on the configured port.
    """
    ftp_port = PORTS["FTP"]
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", ftp_port))
    server_socket.listen(5)

    print(f"[FTP] Honeypot listening on port {ftp_port}...")

    while True:
        client_socket, _ = server_socket.accept()
        thread = threading.Thread(target=handle_ftp_connection, args=(client_socket,))
        thread.start()
