from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import threading
import signal
import sys
from fake_services.fake_ssh import start_ssh_honeypot
from fake_services.fake_http import start_http_honeypot
from fake_services.fake_ftp import start_ftp_honeypot
from utils.network_monitor import start_packet_sniffing
from logger import get_logs as fetch_logs

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
  # Enable CORS for React frontend

shutdown_event = threading.Event()

@app.route("/api/logs")
def api_logs():
    try:
        service_filter = request.args.get("service")
        logs = fetch_logs(service_filter=service_filter)
        return jsonify(logs), 200
    except Exception as e:
        app.logger.error(f"Error in /api/logs: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/stats")
def api_stats():
    try:
        logs = fetch_logs()
        unique_ips = len(set(log.get('source_ip') for log in logs))
        alerts = len([log for log in logs if log.get('alert')])
        
        stats = {
            "totalConnections": len(logs),
            "uniqueIPs": unique_ips,
            "alerts": alerts,
            "activeThreats": alerts
        }
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Remove the old route that served HTML template
# @app.route("/")
# def home():
#     return render_template("dashboard.html")

def start_service(target, name, *args):
    def wrapper():
        try:
            target(*args)
        except Exception as e:
            print(f"[ERROR] {name} failed: {e}")
    thread = threading.Thread(target=wrapper, daemon=True, name=name)
    thread.start()
    print(f"[INFO] Started {name}")

def shutdown_handler(signum, frame):
    print("\n[SHUTDOWN] Shutting down...")
    shutdown_event.set()
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)
    
    print("🚀 Starting Honeypot Services and API Server...")
    start_service(start_packet_sniffing, "Packet Sniffer", shutdown_event)
    start_service(start_ssh_honeypot, "SSH Honeypot")
    start_service(start_http_honeypot, "HTTP Honeypot")
    start_service(start_ftp_honeypot, "FTP Honeypot")
    
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)