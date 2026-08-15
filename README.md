 🚗 AutoRescue

Smart Vehicle Breakdown Assistance Platform

**AutoRescue** is a web-based vehicle breakdown assistance platform that connects customers with nearby mechanics when their vehicle breaks down.

The platform provides a simple and efficient way for users to request roadside assistance, while mechanics can manage service requests and respond to customers. An admin dashboard is included for managing users, mechanics, and platform activities.

> 🚘 **Breakdown happens. AutoRescue responds.**

---

 ✨ Features

👤 Customer

* 🔐 Secure registration and login
* 📍 Location-based roadside assistance requests
* 🔧 Request nearby mechanic assistance
* 📋 Track service requests
* 👨‍🔧 View mechanic information
* 📱 Responsive customer dashboard
* 🚨 Emergency vehicle assistance workflow

 👨‍🔧 Mechanic

* 🔐 Mechanic registration and login
* 🛠️ Create and manage mechanic profile
* 📍 Manage service location
* 📋 View customer assistance requests
* ✅ Accept and manage service requests
* 📊 Mechanic dashboard

 👑 Admin

* 🔐 Admin authentication
* 👥 Manage customers and mechanics
* 📊 Admin dashboard
* 📋 Monitor service requests
* 🗃️ Manage platform data


🧠 How AutoRescue Works

text
Customer
   │
   ▼
Vehicle Breakdown
   │
   ▼
Open AutoRescue
   │
   ▼
Share Location
   │
   ▼
Create Assistance Request
   │
   ▼
Nearby Mechanic
   │
   ▼
Mechanic Accepts Request
   │
   ▼
Roadside Assistance
   │
   ▼
Problem Solved ✅

🛠️ Tech Stack

Backend

* 🐍 Python
* 🌐 Flask
* 🗄️ Flask-SQLAlchemy
* 🔑 Werkzeug

Database

* 🪶 SQLite — default development database
* 🐬 MySQL — supported for production-style configuration
* 🔌 PyMySQL

Frontend

* HTML5
* CSS3
* JavaScript
* Responsive UI

Location

* 📍 Browser Geolocation API
* 🗺️ OpenStreetMap

📂 Project Structure

text
AutoRescue/
│
├── models/
│   └── Database Models
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/
│   ├── Customer Pages
│   ├── Mechanic Pages
│   ├── Admin Pages
│   └── Authentication Pages
│
├── app.py
├── config.py
├── create_database.py
├── init_db.py
├── autorescue.db
├── requirements.txt
├── SETUP.md
└── WORKFLOW.md

 🚀 Installation & Setup

1. Clone the repository

bash
git clone https://github.com/Vedantkhandale/AutoRescue.git
cd AutoRescue

2. Create a virtual environment
bash
python -m venv .venv

3. Activate the environment

Windows PowerShell

powershell
.\.venv\Scripts\Activate.ps1

 Windows CMD

cmd
.venv\Scripts\activate

4. Install dependencies

bash
pip install -r requirements.txt

5. Initialize the database

bash
python init_db.py

 6. Run the application

bash
python app.py

7. Open in browser

text
http://127.0.0.1:5000

 🔑 Demo Credentials

Customer

text
Email: customer@example.com
Password: password123
```

### Mechanic

```text
Email: mechanic@example.com
Password: password123
```

### Admin

```text
Email: admin@example.com
Password: admin123
```

> ⚠️ These credentials are intended for local/demo use only.

---

## 🗄️ Database Configuration

AutoRescue uses **SQLite by default**, so you don't need XAMPP or MySQL for basic local development.

```text
SQLite
   ↓
autorescue.db
```

For MySQL, configure the required environment variables:

```powershell
$env:DB_ENGINE="mysql"
$env:DB_HOST="localhost"
$env:DB_PORT="3306"
$env:DB_USER="root"
$env:DB_PASSWORD=""
$env:DB_NAME="autorescue_v2"
```

---

## 🔐 Security

AutoRescue includes:

* Password hashing
* Authentication and authorization
* Role-based dashboards
* Protected application routes
* Database-backed user management
* Environment-based database configuration

---

## 🎯 Project Objectives

The main objectives of AutoRescue are:

1. Reduce the time required to find a mechanic during a vehicle breakdown.
2. Connect customers with available mechanics.
3. Provide a centralized platform for roadside assistance.
4. Make emergency vehicle assistance easier and faster.
5. Provide separate dashboards for customers, mechanics, and administrators.

---

## 🚀 Future Enhancements

* 🤖 AI-based mechanic recommendation
* 📍 Real-time mechanic tracking
* 💳 Online payment integration
* ⭐ Mechanic ratings and reviews
* 📞 In-app calling
* 💬 Real-time chat
* 🔔 Push notifications
* 🗺️ Advanced route optimization
* 📱 Android/iOS mobile application
* 🧠 Predictive vehicle maintenance
* 🚨 One-tap emergency assistance

---

## 🧪 Development

Run Python compilation checks:

```bash
python -m compileall app.py models static templates
```

Initialize database:

```bash
python init_db.py
```

Start application:

```bash
python app.py
```

---

## 📚 Documentation

Additional project documentation:

* [Setup Guide](SETUP.md)
* [Project Workflow](WORKFLOW.md)

---

## 👨‍💻 Developer

### Vedant Khandale

**Full Stack Web Developer | Python & Flask Developer**

📌 India

🔗 GitHub:
https://github.com/Vedantkhandale

---

## ⭐ Support

If you find **AutoRescue** useful, consider giving the repository a ⭐ on GitHub.

---

## 📄 License

This project is developed for educational and portfolio purposes.
