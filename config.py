import os

PORTS = {"SSH": 2222, "HTTP": 8080, "FTP": 2121}
FAKE_BANNERS = {
    "SSH": "SSH-2.0-OpenSSH_7.9p1 Ubuntu-10",
    "HTTP": "HTTP/1.1 200 OK\nContent-Type: text/html\n\n<h1>Fake HTTP Server</h1>",
    "FTP": "220 Fake FTP Server Ready.\n"
}

LOG_DIR = os.path.join(os.getcwd(), "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "logs.json")

ALERT_SETTINGS = {
    "EMAIL_ALERTS": True,
    "EMAIL_SENDER": os.getenv("EMAIL_SENDER", "your_email@example.com"),
    "EMAIL_RECEIVER": os.getenv("EMAIL_RECEIVER", "receiver_email@example.com"),
    "EMAIL_PASSWORD": os.getenv("EMAIL_PASSWORD", ""),
    "SMTP_SERVER": "smtp.gmail.com",
    "SMTP_PORT": 587,
    "TELEGRAM_ALERTS": True,
    "TELEGRAM_BOT_TOKEN": os.getenv("TELEGRAM_BOT_TOKEN", "your_bot_token"),
    "TELEGRAM_CHAT_ID": os.getenv("TELEGRAM_CHAT_ID", "your_chat_id"),
}