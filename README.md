# HoneyTrap - Automated Honeypot Deployment Tool

## 📌 Introduction
**HoneyTrap** is an Automated Honeypot Deployment Tool designed for cybersecurity professionals and researchers. It simulates vulnerable services to attract and log malicious activities, helping in threat analysis and network security improvement. The tool provides real-time packet monitoring, logging, and filtering based on network protocols.

## 🚀 Features
- **Automated Honeypot Deployment** for multiple services (SSH, HTTP, FTP)
- **Real-time Packet Monitoring** using Scapy
- **Web Dashboard** with interactive traffic analysis
- **Logging System** to store honeypot activity in JSON format
- **Protocol-based Filtering** (TCP, UDP, ICMP)
- **Graphical Representation** using Chart.js
- **Threaded Service Execution** for optimal performance
- **Security Alerts** (Email & Telegram notifications)

## 🏗️ Project Structure
```
📂 honeypot
├── 📂 fake_services
│   ├── fake_ssh.py  # SSH Honeypot
│   ├── fake_http.py # HTTP Honeypot
│   ├── fake_ftp.py  # FTP Honeypot
│
├── 📂 utils
│   ├── network_monitor.py  # Packet Sniffing Logic
│
├── 📂 logs
│   ├── logs.json  # Captured honeypot activities
│
├── 📂 templates
│   ├── dashboard.html  # Web Interface for Data Visualization
│
├── 📂 static
│   ├── styles.css  # CSS for dashboard styling
│
├── config.py  # Configuration (Ports, Alerts, Banners)
├── logger.py  # Logging Mechanism
├── honeypot.py  # Main file to launch honeypot services
├── server.py  # Flask Web Server for Dashboard
├── requirements.txt  # Python dependencies
├── README.md  # Project Documentation
```

## 🔧 Installation
### **Prerequisites**
- Python 3.x
- pip package manager
- Scapy for packet sniffing
- Flask for web dashboard

### **Setup Instructions**
```sh
# Clone the repository
git clone https://github.com/yourusername/HoneyTrap.git
cd HoneyTrap

# Install dependencies
pip install -r requirements.txt

# Create logs directory (if not exists)
mkdir logs && touch logs/logs.json

# Run the honeypot
taskkill /IM python.exe /F  # (Windows - if required)
python honeypot.py

# Run the web dashboard
python server.py
```

## 🖥️ Usage
- The honeypot will start listening on **SSH (2222), HTTP (8080), and FTP (2121)**.
- Captured logs will be stored in `logs/logs.json`.
- Open `http://127.0.0.1:5000` to monitor logs visually.
- Use the **protocol filter dropdown** on the dashboard to analyze specific network traffic.

## ⚙️ Technologies Used
- **Backend:** Python, Flask
- **Frontend:** HTML, JavaScript, Chart.js
- **Networking:** Scapy for packet sniffing
- **Data Storage:** JSON for log management
- **Security Alerts:** SMTP (Email), Telegram API

## 🔥 DSA Concepts Used
- **Hashing & Dictionaries:** Storing logs efficiently
- **Multi-threading:** Running honeypot services concurrently
- **Queue-based Event Handling:** Packet sniffing and logging

## 🚧 Future Enhancements
- Advanced honeypot deception techniques
- AI-based intrusion pattern recognition
- Real-time attack visualization on a world map
- Docker containerization for easy deployment

## 📜 License
This project is open-source and available under the **MIT License**.

---
🚀 **Developed with cybersecurity in mind! Stay Safe!**

