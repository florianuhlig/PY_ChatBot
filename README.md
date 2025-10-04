# 🤖 PY_ChatBot

A modular, secure, and extensible web-based chatbot platform built with Flask. Features include user authentication, session management, multi-database support, and a modern responsive UI.

---

## 📋 Table of Contents

- [Features](#features)  
- [Demo](#demo)  
- [Installation](#installation)  
- [Configuration](#configuration)  
- [Usage](#usage)  
- [Project Structure](#project-structure)  
- [Docker Setup](#docker-setup)  
- [Contributing](#contributing)  
- [Troubleshooting](#troubleshooting)  
- [License](#license)  

---

## ✨ Features

- **User Authentication**  
  - Registration, login, logout, and password change  
  - Email validation and strong password requirements  
  - Secure session cookies with configurable lifetime  

- **Multi-Database Support**  
  - Abstracted database layer  
  - Thread-safe SQLite implementation  
  - Ready for PostgreSQL/MySQL integration  

- **Modern UI/UX**  
  - Responsive templates: login, register, dashboard, profile, change password, 404  
  - Gradient backgrounds, animations, and hover effects  
  - Flash messages for real-time feedback  

- **Security**  
  - SHA-512 password hashing  
  - Decorators for route protection (`@login_required`, `@logout_required`)  
  - CSRF-ready and input validation utilities  

- **Developer-Friendly**  
  - Well-organized code: `config`, `database`, `frontend`, `models`, `services`, `utils`  
  - Comprehensive logging and error handlers  
  - Environment-based configuration  

---

## 🖥 Demo

Screenshots and live demo links can be added here.

---

## 🛠 Installation

### Prerequisites

- Python 3.8+  
- Git  

### Local Setup

1. **Clone the repo**

   ```bash
   git clone https://github.com/florianuhlig/PY_ChatBot.git
   cd PY_ChatBot
   git checkout Development
   ```

2. **Create virtual environment**

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # macOS/Linux
   .venv\Scripts\activate      # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**

   Copy `.env.example` to `.env` and adjust values:

   ```bash
   cp .env.example .env
   ```

5. **Run the app**

   ```bash
   python main.py
   ```

   Open your browser to `http://localhost:8080`.

---

## ⚙️ Configuration

Edit `.env` for:

- `DB_TYPE` (e.g., `sqlite`, `postgresql`, `mysql`)  
- `SQLITE_PATH` (path to SQLite file)  
- `FLASK_SECRET_KEY`  
- `FLASK_DEBUG`, `FLASK_HOST`, `FLASK_PORT`  
- Session and password policy variables  

---

## 🚀 Usage

- **Register**: `/register`  
- **Login**: `/login`  
- **Dashboard**: `/dashboard` (protected)  
- **Profile**: `/profile` (protected)  
- **Change Password**: `/change-password` (protected)  
- **Logout**: `/logout`  

---

## 📁 Project Structure

```
PY_ChatBot/
├── config/               # App configuration loader
│   └── database.py
├── database/             # DB abstraction and implementations
│   ├── interface.py
│   ├── sqlite_db.py
│   └── flask_integration.py
├── frontend/             # Flask application and templates
│   ├── app.py
│   └── templates/
│       ├── login.html
│       ├── register.html
│       ├── dashboard.html
│       ├── profile.html
│       ├── change_password.html
│       └── 404.html
├── models/               # Data models (if any)
├── services/             # Business logic: user and auth services
├── utils/                # Utility functions and decorators
├── .env.example          # Environment variable template
├── Dockerfile            # Container setup
├── docker-compose.yml    # Orchestration
├── docker-entrypoint.sh  # Init script
├── main.py               # Entry point
└── requirements.txt      # Python dependencies
```