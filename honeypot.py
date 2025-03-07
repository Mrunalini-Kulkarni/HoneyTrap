import threading
import signal
import sys
from threading import Thread
from fake_services.fake_ssh import start_ssh_honeypot
from fake_services.fake_http import start_http_honeypot
from fake_services.fake_ftp import start_ftp_honeypot
from utils.network_monitor import start_packet_sniffing

# Store active threads for graceful shutdown
active_threads = []

def start_service(target_function, name):
    """Start a honeypot service in a separate daemon thread."""
    thread = Thread(target=target_function, daemon=True, name=name)
    thread.start()
    active_threads.append(thread)

def shutdown_handler(signum, frame):
    """Handle graceful shutdown on Ctrl+C or termination signals."""
    print("\nShutting down honeypot services...")
    sys.exit(0)

# Register shutdown signals
signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)

if __name__ == "__main__":
    print("🚀 Starting Honeypot Services...")

    # Start packet sniffing in the background
    threading.Thread(target=start_packet_sniffing, daemon=True, name="PacketSniffer").start()

    # Start honeypot services
    start_service(start_ssh_honeypot, "SSH Honeypot")
    start_service(start_http_honeypot, "HTTP Honeypot")
    start_service(start_ftp_honeypot, "FTP Honeypot")

    # Keep the main thread alive
    for thread in active_threads:
        thread.join()
