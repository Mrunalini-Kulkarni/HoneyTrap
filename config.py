import os

# Define ports for fake services
PORTS = {
    "SSH": 2222,   # Fake SSH port
    "HTTP": 8080,  # Fake HTTP port
    "FTP": 2121    # Fake FTP port
}

# Fake banners for services
FAKE_BANNERS = {
    "SSH": "SSH-2.0-OpenSSH_7.9p1 Ubuntu-10",
    "HTTP": "HTTP/1.1 200 OK\nContent-Type: text/html\n\n<h1>Fake HTTP Server</h1>",
    "FTP": "220 Fake FTP Server Ready.\n"
}


# Ensure logs are stored in a proper directory
LOG_DIR = os.path.join(os.getcwd(), "logs")  # Ensure absolute path
os.makedirs(LOG_DIR, exist_ok=True)  # Create directory if not exists

LOG_FILE = os.path.join(LOG_DIR, "logs.json")  # Ensure full path

# Alert settings
ALERT_SETTINGS = {
    "EMAIL_ALERTS": True,  # Set to False to disable email alerts

    # Use environment variables for sensitive info (avoid hardcoding passwords!)
    "EMAIL_SENDER": os.getenv("EMAIL_SENDER", "your_email@example.com"),
    "EMAIL_RECEIVER": os.getenv("EMAIL_RECEIVER", "receiver_email@example.com"),
    "EMAIL_PASSWORD": os.getenv("EMAIL_PASSWORD", ""),  # Securely load from environment
    "SMTP_SERVER": "smtp.gmail.com",
    "SMTP_PORT": 587,

    "TELEGRAM_ALERTS": True,  # Set to False to disable Telegram alerts
    "TELEGRAM_BOT_TOKEN": os.getenv("TELEGRAM_BOT_TOKEN", "your_bot_token"),
    "TELEGRAM_CHAT_ID": os.getenv("TELEGRAM_CHAT_ID", "your_chat_id"),
}
