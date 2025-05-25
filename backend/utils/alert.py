# alert.py - Sends alerts for honeypot attacks

import smtplib
import requests
from config import ALERT_SETTINGS

def send_email_alert(attacker_ip, service):
    if not ALERT_SETTINGS["EMAIL_ALERTS"]:
        return
    sender_email = ALERT_SETTINGS["EMAIL_SENDER"]
    receiver_email = ALERT_SETTINGS["EMAIL_RECEIVER"]
    password = ALERT_SETTINGS["EMAIL_PASSWORD"]
    subject = f"[Honeypot Alert] {service} Attack Detected"
    body = f"Suspicious activity detected from IP: {attacker_ip} on {service}"
    message = f"Subject: {subject}\n\n{body}"
    try:
        with smtplib.SMTP(ALERT_SETTINGS["SMTP_SERVER"], ALERT_SETTINGS["SMTP_PORT"]) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
        print(f"[EMAIL ALERT] Sent alert for {attacker_ip} on {service}")
    except Exception as e:
        print(f"[EMAIL ERROR] Failed to send email: {e}")

def send_telegram_alert(attacker_ip, service):
    if not ALERT_SETTINGS["TELEGRAM_ALERTS"]:
        return
    bot_token = ALERT_SETTINGS["TELEGRAM_BOT_TOKEN"]
    chat_id = ALERT_SETTINGS["TELEGRAM_CHAT_ID"]
    message = f"[Honeypot Alert] {service} attack detected from {attacker_ip}"
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {"chat_id": chat_id, "text": message}
    try:
        requests.post(url, params=params)
        print(f"[TELEGRAM ALERT] Sent alert for {attacker_ip} on {service}")
    except Exception as e:
        print(f"[TELEGRAM ERROR] Failed to send Telegram alert: {e}")