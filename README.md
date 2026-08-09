# Trekking Management Application

A web-based trekking management system built with Flask and SQLite to streamline trek bookings, guide assignments, and administrative oversight.

---

## 🚀 Key Features

- **Role-Based Access Control (RBAC):** Dedicated portals for **Admin**, **Staff (Guides)**, and **Trekkers**.
- **Admin Dashboard:** Manage treks (CRUD), assign guides, approve/reject staff applications, view all bookings, and manage user status (blacklist/unblock).
- **Staff Portal:** View assigned treks, access participant lists, and manage profile information.
- **Trekker Portal:** Search and filter treks by keyword, location, and difficulty, book available slots, and view booking history.

---

## 🛠️ Tech Stack

- **Backend:** Python, Flask
- **Database & ORM:** SQLite, Flask-SQLAlchemy, Flask-Migrate
- **Security:** bcrypt (password hashing), session-based role authorization
- **Frontend:** HTML5, Jinja2 Templates, Bootstrap 5, Bootstrap Icons

---

## 💻 Setup & Installation Instructions

Follow these simple steps to run the project locally:

### 1. Clone or Open the Repository
```bash
cd "MAD1 PROJECT"
```

### 2. Create and Activate a Virtual Environment
- **On Linux / macOS:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```
- **On Windows:**
  ```bash
  python -m venv .venv
  .venv\Scripts\activate
  ```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Create the Admin User
Run the setup script to initialize the database and create the default admin account:
```bash
python create-admin.py
```

### 5. Run the Application
```bash
python app.py
```
Open your browser and navigate to: **`http://127.0.0.1:5000`**

---

## 🔑 Default Admin Credentials

| Email | Password | Role |
| :--- | :--- | :--- |
| `admin@admin.com` | `admin@123` | `admin` |

---

## 👥 User Roles Overview

1. **Admin:** Created using `create-admin.py`.
2. **Staff:** Registered via the `/register` page with the "Trek Staff" option (requires admin approval before accessing the staff dashboard).
3. **Trekker:** Registered via the `/register` page with the "Trekker" option (can immediately browse and book treks).
