# logger.py - Thread-safe logging for honeypot events

import json
import os
import threading
from datetime import datetime
from config import LOG_FILE

# Ensure logs directory exists
log_dir = os.path.dirname(LOG_FILE)
os.makedirs(log_dir, exist_ok=True)

# Thread-safe lock for file access
log_lock = threading.Lock()

def initialize_log_file():
    """Initialize logs.json as an empty list if it doesn’t exist or is invalid."""
    with log_lock:
        if not os.path.exists(LOG_FILE) or os.stat(LOG_FILE).st_size == 0:
            with open(LOG_FILE, "w", encoding="utf-8") as f:
                json.dump([], f, indent=4)
        else:
            try:
                with open(LOG_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if not isinstance(data, list):
                        raise ValueError("Log file is not a JSON list")
            except (json.JSONDecodeError, UnicodeDecodeError, ValueError):
                print(f"[LOG WARNING] {LOG_FILE} is corrupted or invalid. Resetting to empty list.")
                with open(LOG_FILE, "w", encoding="utf-8") as f:
                    json.dump([], f, indent=4)
            except IOError as e:
                print(f"[LOG ERROR] Failed to access {LOG_FILE}: {e}")
                with open(LOG_FILE, "w", encoding="utf-8") as f:
                    json.dump([], f, indent=4)

def log_packet(service, client_ip, additional_info=None):
    """Safely logs attack or packet details to logs.json."""
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "service": service,
        "source_ip": client_ip,
        "destination_ip": "127.0.0.1",
        "protocol": "TCP",
        "length": 0
    }
    if additional_info:
        log_entry.update(additional_info)

    with log_lock:
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                logs = json.load(f) if os.stat(LOG_FILE).st_size > 0 else []
            if not isinstance(logs, list):
                logs = []
            logs.append(log_entry)
            logs = logs[-5000:]
            with open(LOG_FILE, "w", encoding="utf-8") as f:
                json.dump(logs, f, indent=4)
        except (FileNotFoundError, json.JSONDecodeError, IOError) as e:
            print(f"[LOG ERROR] Failed to write log: {e}")
            with open(LOG_FILE, "w", encoding="utf-8") as f:
                json.dump([log_entry], f, indent=4)
        except Exception as e:
            print(f"[LOG ERROR] Unexpected error: {e}")

def get_logs(service_filter=None):
    """Retrieves logs from logs.json, optionally filtered by service."""
    with log_lock:
        try:
            if not os.path.exists(LOG_FILE) or os.stat(LOG_FILE).st_size == 0:
                return []
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                logs = json.load(f)
                if not isinstance(logs, list):
                    return []
                if service_filter:
                    return [log for log in logs if log.get("service") == service_filter]
                return logs
        except (FileNotFoundError, json.JSONDecodeError, IOError) as e:
            print(f"[LOG ERROR] Failed to read logs: {e}")
            return []
        except Exception as e:
            print(f"[LOG ERROR] Unexpected error: {e}")
            return []

# Initialize log file on import
initialize_log_file()

if __name__ == "__main__":
    # Test the logger
    log_packet("SSH", "192.168.1.1")
    log_packet("HTTP", "10.0.0.1", {"length": 128})
    logs = get_logs()
    print("All Logs:", logs)
    ssh_logs = get_logs("SSH")
    print("SSH Logs:", ssh_logs)