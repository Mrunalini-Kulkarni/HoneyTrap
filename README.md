# 🐝 HoneyTrap

> **Automated Honeypot Deployment Tool for Network Security & Intrusion Detection**

---

## 🚀 Overview

HoneyTrap is a **Python-based honeypot deployment tool** designed to help cybersecurity enthusiasts and professionals detect unauthorized network access in real-time.  
It automatically deploys honeypots, captures suspicious activity, and visualizes the data through a modern React.js frontend.

---

## ✨ Features

- 🛡️ **Automated honeypot deployment** with customizable settings  
- 📊 **Real-time visualization** of captured network events  
- 📂 **Logs stored in JSON format** for easy analysis (`backend/logs/logs.json`)  
- 🔍 **Filtering and sorting** by protocols and packet types  
- ⚙️ Fully integrated backend logs with frontend UI (no mock data)  
- 📈 Interactive dashboard for trend analysis and insights  

---

## 🛠️ Technology Stack

| Layer     | Technology                  |
|-----------|-----------------------------|
| Backend   | Python (Flask)               |
| Frontend  | React.js                    |
| Data      | JSON (log storage)          |
| Others    | Axios (API calls), Chart.js (visualization) |

---

## 💾 Installation & Setup

1. **Clone the repository**

```bash
git clone https://github.com/Mrunalini-Kulkarni/HoneyTrap.git
cd HoneyTrap
Set up Python backend

bash
Copy
Edit
pip install -r requirements.txt
python app.py
Run the React frontend

bash
Copy
Edit
cd frontend
npm install
npm start
📚 Usage
Honeypot starts capturing network traffic automatically once backend runs

Frontend fetches live logs from backend/logs/logs.json and displays data dynamically

Use dashboard controls to filter and analyze captured packets by protocol and time

Logs are saved locally for offline review or extended analysis

📝 Project Structure
plaintext
Copy
Edit
HoneyTrap/
├── backend/
│   ├── app.py              # Flask backend server
│   ├── logs/
│   │   └── logs.json       # Captured honeypot logs stored here
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── src/                # React frontend source files
│   ├── public/
│   ├── package.json
│   └── README.md
└── README.md               # Project documentation
🤝 Contributing
Contributions, issues, and feature requests are welcome!
Feel free to fork the repo and submit a pull request.

📄 License
This project is licensed under the MIT License. See LICENSE for details.