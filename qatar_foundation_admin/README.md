# Qatar Foundation Admin Portal

A Flask-based admin management portal for handling opportunities, learners, verifiers, and collaborators with secure authentication, password reset, and dashboard features.

---

## 📌 Project Overview

This project was built as an admin portal where administrators can:

* Register and log in securely
* Manage opportunities (Create / Read / Update / Delete)
* View dashboard statistics
* Manage learners, verifiers, and collaborators
* Reset forgotten passwords through email
* Stay logged in with persistent sessions

---

## 🚀 Features

### Authentication

* Admin Sign Up
* Admin Login
* Remember Me session support
* Forgot Password via email reset link
* Secure password hashing
* Logout

### Opportunity Management

* Add new opportunities
* View all opportunities
* Edit existing opportunities
* Delete opportunities
* Data stored in SQLite database
* Only creator/admin can manage their own records

### Dashboard

* Sidebar navigation
* Search UI
* Stats cards
* Responsive layout
* Dark / Light mode (if enabled)

---

## 🛠️ Tech Stack

### Backend

* Python
* Flask
* Flask-SQLAlchemy
* Flask-Login
* Flask-Mail
* Werkzeug Security

### Frontend

* HTML5
* CSS3
* JavaScript

### Database

* SQLite

---

## 📁 Project Structure

```text
qatar_foundation_admin/
│── app.py
│── config.py
│── models.py
│── routes.py
│── requirements.txt
│── README.md
│
├── instance/
│   └── data.db
│
├── static/
│   ├── admin.css
│   └── admin.js
│
└── templates/
    └── index.html
```

---

## ⚙️ Installation Steps

### 1. Clone or Download Project

Place project folder in your local machine.

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Mac/Linux

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run Application

```bash
python app.py
```

### 6. Open Browser

```text
http://127.0.0.1:5000
```

---

## 📧 Email Password Reset Setup

Update `config.py`

```python
MAIL_USERNAME = "suryamahesh039@gmail.com"
MAIL_PASSWORD = "****"
```

Use Gmail App Password (recommended).

---

## 🔐 Default Security Features

* Password hashing
* Session authentication
* Protected routes
* Ownership checks for records
* Expiring password reset tokens

---

## 📌 Notes

* Phone reset links work when using local IP and same Wi-Fi network.
* SQLite database auto-creates on first run.
* Flask debug mode enabled for development only.

---

## 🚀 Future Improvements

* Deploy to Render / Railway
* Admin roles & permissions
* File uploads
* Reports export (CSV/PDF)
* Notifications system
* Better analytics dashboard

---

## 👨‍💻 Author

Developed by Surya

---

