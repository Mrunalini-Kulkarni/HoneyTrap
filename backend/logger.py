# logger.py - Thread-safe logging for honeypot events

import json
import os
import threading
from datetime import datetime
from config import LOG_FILE
from pybloom_live import BloomFilter
from collections import defaultdict
from time import time

log_lock = threading.Lock()
ip_filter = BloomFilter(capacity=10000, error_rate=0.001)
ip_timestamps = defaultdict(list)

def initialize_log_file():
    with log_lock:
        if not os.path.exists(LOG_FILE) or os.stat(LOG_FILE).st_size == 0:
            with open(LOG_FILE, "w", encoding="utf-8") as f:
                json.dump([], f, indent=4)

def log_packet(service, client_ip, additional_info=None):
    now = time()
    ip_timestamps[client_ip].append(now)
    ip_timestamps[client_ip] = [t for t in ip_timestamps[client_ip] if now - t < 60]
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "service": service,
        "source_ip": client_ip,
        "destination_ip": "127.0.0.1",  # Default, overridden by additional_info if provided
        "protocol": "TCP",
        "length": 0
    }
    if additional_info:
        log_entry.update(additional_info)
    if len(ip_timestamps[client_ip]) > 10:
        log_entry["alert"] = "Possible brute-force"
        from utils.alert import send_email_alert, send_telegram_alert
        send_email_alert(client_ip, service)
        send_telegram_alert(client_ip, service)
    if client_ip not in ip_filter:
        ip_filter.add(client_ip)
        print(f"[NEW IP] {client_ip} detected")
    with log_lock:
        try:
            with open(LOG_FILE, "r+", encoding="utf-8") as f:
                logs = json.load(f) if os.stat(LOG_FILE).st_size > 0 else []
                logs.append(log_entry)
                logs = logs[-5000:]
                f.seek(0)
                json.dump(logs, f, indent=4)
                f.truncate()
        except Exception as e:
            print(f"[LOG ERROR] Failed to write log: {e}")
            with open(LOG_FILE, "w", encoding="utf-8") as f:
                json.dump([log_entry], f, indent=4)

def get_logs(service_filter=None):
    with log_lock:
        try:
            if not os.path.exists(LOG_FILE) or os.stat(LOG_FILE).st_size == 0:
                return []
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                logs = json.load(f)
                if service_filter:
                    return [log for log in logs if log.get("service") == service_filter]
                return logs
        except Exception as e:
            print(f"[LOG ERROR] Failed to read logs: {e}")
            return []

initialize_log_file()