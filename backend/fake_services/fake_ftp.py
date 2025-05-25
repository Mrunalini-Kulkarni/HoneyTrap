# fake_services/fake_ftp.py - Fake FTP Honeypot Service

import socket
import threading
from logger import log_packet as log_attack
from config import PORTS, FAKE_BANNERS

def handle_ftp_connection(client_socket):
    try:
        client_ip, _ = client_socket.getpeername()
        server_ip, server_port = client_socket.getsockname()  # Get server IP
        client_socket.send(FAKE_BANNERS["FTP"].encode())
        data = client_socket.recv(1024).decode(errors="ignore")
        log_attack("FTP", client_ip, {"input": data, "length": len(data), "destination_ip": server_ip})
        if "user" in data.lower():
            client_socket.send(b"Password: ")
            password = client_socket.recv(1024).decode(errors="ignore")
            log_attack("FTP", client_ip, {"password_attempt": password, "destination_ip": server_ip})
    except Exception as e:
        print(f"[FTP] Error handling connection from {client_ip}: {e}")
    finally:
        client_socket.close()

def start_ftp_honeypot():
    ftp_port = PORTS["FTP"]
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server_socket.bind(("0.0.0.0", ftp_port))
        server_socket.listen(5)
        print(f"[FTP] Honeypot listening on port {ftp_port}...")
        while True:
            client_socket, _ = server_socket.accept()
            thread = threading.Thread(target=handle_ftp_connection, args=(client_socket,))
            thread.start()
    except Exception as e:
        print(f"[FTP] Failed to start: {e}")