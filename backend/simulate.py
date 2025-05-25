import socket
import threading
import time

SERVER_IP = "192.168.56.1"  # Replace with your server’s IP (e.g., 192.168.1.x or 127.0.0.1)
PORTS = [2222, 8080, 2121]  # SSH, HTTP, FTP
ATTEMPTS = 15  # Number of attempts per port

def attack_port(port):
    for i in range(ATTEMPTS):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((SERVER_IP, port))
            sock.send(b"user\n")
            response = sock.recv(1024).decode(errors="ignore")
            print(f"Port {port}: Sent 'user', received: {response}")
            sock.send(b"testpass\n")
            response = sock.recv(1024).decode(errors="ignore")
            print(f"Port {port}: Sent 'testpass', received: {response}")
            sock.close()
        except Exception as e:
            print(f"Port {port}: Error - {e}")
        time.sleep(0.1)  # Small delay between attempts

if __name__ == "__main__":
    threads = []
    for port in PORTS:
        t = threading.Thread(target=attack_port, args=(port,))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    print("Brute-force simulation complete.")