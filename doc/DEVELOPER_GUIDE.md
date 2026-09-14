# 🛠️ Developer & Operational Guide
## Project: Trekking Management Application (Bauhaus Edition)
**Tech Stack:** Python 3.10+ • Flask 3.1.3 • SQLite • SQLAlchemy • Jinja2 • Bootstrap 5  

---

## 1. Development Environment Setup

### 1.1. Prerequisites
Ensure you have the following installed on your machine:
- **Python 3.10+** (verify with `python3 --version`)
- **pip** (Python package manager)
- **SQLite 3**
- Modern Web Browser (Chrome, Firefox, Safari, Edge)

### 1.2. Installation Steps

1. **Clone or Navigate to Repository:**
   ```bash
   cd "/mnt/8A7C87E87C87CCFF/CODESPACE/MAD1 PROJECT"
   ```

2. **Create and Activate Virtual Environment:**
   ```bash
   # Create a virtual environment
   python3 -m venv venv

   # Activate virtual environment (Linux/macOS)
   source venv/bin/activate

   # Activate virtual environment (Windows)
   # venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *Core & High-Performance Security Packages:*
   - `Flask==3.1.3`
   - `Flask-SQLAlchemy==3.1.1`
   - `Flask-Migrate==4.1.0`
   - `bcrypt==5.0.0`
   - `SQLAlchemy==2.0.51`
   - `alembic==1.19.0`
   - `redis>=5.0.0` (In-memory caching, rate-limiting & distributed locking)
   - `Flask-Session>=0.8.0` (Server-side Redis session storage)
   - `Flask-Limiter>=3.9.0` (Sliding-window distributed rate limiter)
   - `Flask-WTF>=1.2.2` (CSRF defense)

4. **Start Redis In-Memory Engine:**
   ```bash
   # Option A: Start native service (Linux)
   sudo systemctl start redis-server
   
   # Option B: Run via Docker (Zero-install option)
   docker run -d --name trek-redis -p 6379:6379 redis:7-alpine
   ```
   *Note:* The architecture includes graceful degradation—if Redis is unreachable during local offline testing, cache lookups fall back to the SQLite relational database automatically.

5. **Initialize Database & Seed Administrator:**
   If `instance/app.db` does not exist or needs resetting:
   ```bash
   # Execute the admin seeding script
   python create-admin.py
   ```
   *Default Admin Credentials:*
   - **Email:** `admin@gmail.com`
   - **Password:** `12345678` (or as configured in `create-admin.py`)
   - **Role:** `admin`

6. **Run the Development Server:**
   ```bash
   python app.py
   ```
   The application will boot at: **`http://127.0.0.1:5000`**

---

## 2. Directory Structure Reference

```
MAD1 PROJECT/
├── doc/                             # Comprehensive Documentation Suite
│   ├── README.md                    # Master documentation index
│   ├── PRD.md                       # Product Requirements Document
│   ├── BAUHAUS_DESIGN_SYSTEM.md     # Visual design language & CSS tokens
│   ├── ARCHITECTURE_AND_EXTENSIONS.md # Technical architecture & DB extensions
│   ├── BAUHAUS_IMPLEMENTATION_PLAN.md # Template & migration roadmap
│   └── DEVELOPER_GUIDE.md           # This setup & developer manual
├── instance/
│   └── app.db                       # SQLite database file
├── migrations/                      # Alembic schema migration versions
├── static/
│   └── css/
│       └── style.css                # Bauhaus CSS Engine & custom styles
├── templates/                       # Jinja2 HTML templates
│   ├── base.html                    # Global shell (Navbar, flash, footer)
│   ├── login.html                   # Login screen (Bauhaus poster layout)
│   ├── register.html                # User & Guide registration
│   ├── staff_details.html           # Guide profile completion
│   ├── admin_dashboard.html         # Admin operational command center
│   ├── add_trek.html                # Admin: Create trek
│   ├── edit_trek.html               # Admin: Edit trek
│   ├── assign_staff.html            # Admin: Assign guide to trek
│   ├── staff_dashboard.html         # Guide portal (assigned treks & roster)
│   ├── edit_staff_trek.html         # Guide: Update trek slots & status
│   ├── update_profile.html          # Guide: Update contact info
│   ├── trekker_dashboard.html       # Trekker portal (browse, history, search)
│   ├── update_trekker_profile.html  # Trekker: Update name/email
│   ├── book_trek.html               # Trekker: Booking confirmation
│   └── trek_pass.html               # [New] Printable Bauhaus Digital Pass
├── app.py                           # Core Flask application, controllers & routes
├── models.py                        # SQLAlchemy database schema & relations
├── create-admin.py                  # Seed script for initial admin user
└── requirements.txt                 # Python package dependencies
```

---

## 3. Developing with the Bauhaus Design System

When creating or modifying Jinja2 templates, adhere to these component classes:

### 3.1. Typography & Headers
Always use high-contrast headings with all-caps tracking for section titles:
```html
<h2 class="bh-title">EXPEDITION CATALOG</h2>
<p class="bh-subtitle">ACTIVE ALPINE TRAILS // ALL REGIONS</p>
```

### 3.2. Buttons (`.bh-btn`)
Buttons must always have a 2px black border, 0px border-radius, and a hard drop shadow:
```html
<!-- Primary Action (Red) -->
<button type="submit" class="bh-btn bh-btn-primary">CONFIRM RESERVATION</button>

<!-- Secondary Action (White / Canvas) -->
<a href="/trekker-dashboard" class="bh-btn bh-btn-secondary">RETURN TO DASHBOARD</a>

<!-- Warning / Urgent Action (Yellow) -->
<button class="bh-btn bh-btn-warning">MODIFY STATUS</button>

<!-- Danger Action (Solid Black or Red) -->
<form method="POST" action="/delete-trek/{{ trek.id }}">
    <button type="submit" class="bh-btn bh-btn-danger">TERMINATE TREK</button>
</form>
```

### 3.3. Cards & Panels (`.bh-card`)
Wrap content blocks inside sharp rectangular cards:
```html
<div class="bh-card">
    <div class="bh-card-header bh-header-blue">
        <h5 class="m-0 fw-bold">01 // ASSIGNED EXPEDITIONS</h5>
    </div>
    <div class="bh-card-body p-4">
        <!-- Card Content -->
    </div>
</div>
```

### 3.4. Tables (`.bh-table`)
Wrap tabular data in `.bh-table-container` with inverted black headers:
```html
<div class="bh-table-container">
    <table class="table bh-table align-middle mb-0">
        <thead>
            <tr>
                <th>REF #</th>
                <th>EXPEDITION</th>
                <th>DIFFICULTY</th>
                <th>SLOTS</th>
                <th>STATUS</th>
                <th>ACTION</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="font-monospace fw-bold">#001</td>
                <td class="fw-bold">Roopkund Glacier</td>
                <td><span class="bh-badge bh-badge-hard">HARD</span></td>
                <td class="font-monospace">14 SLOTS</td>
                <td><span class="bh-badge bh-badge-open">OPEN</span></td>
                <td>
                    <a href="/book-trek/1" class="bh-btn bh-btn-sm bh-btn-primary">BOOK</a>
                </td>
            </tr>
        </tbody>
    </table>
</div>
```

### 3.5. Form Controls (`.bh-form-control`)
```html
<div class="mb-3">
    <label class="bh-label">TRAIL NAME</label>
    <input type="text" name="name" class="form-control bh-form-control" placeholder="e.g. Kedarkantha Summit" required>
</div>
```

---

## 4. Database Schema Migrations

When altering `models.py` to add new fields (such as emergency info, altitude, or reviews):

1. **Generate Migration Script:**
   ```bash
   flask db migrate -m "Add emergency contact and trail altitude specs"
   ```

2. **Review Generated Migration:**
   Inspect the new file generated under `migrations/versions/`.

3. **Apply Migration to Database:**
   ```bash
   flask db upgrade
   ```

4. **Rollback (if needed):**
   ```bash
   flask db downgrade
   ```

---

## 5. Testing & Validation Checklist

Before committing any template or controller changes, run through this verification checklist:

- [ ] **Role Isolation:** Trekker accounts cannot access `/admin-dashboard` or `/staff-dashboard`.
- [ ] **Bcrypt Passwords:** New user registrations store hashed passwords in the database (never raw text).
- [ ] **Slot Integrity:** Booking decrements `available_slots` by 1; cancellation increments `available_slots` by 1.
- [ ] **Zero Full Booking:** Treks with 0 available slots disable booking with a flash notice.
- [ ] **Zero Border-Radius:** Ensure no `rounded`, `rounded-circle`, or default soft borders appear in the rendered UI.
- [ ] **High-Contrast Legibility:** All text against colored backgrounds maintains WCAG 2.1 AA minimum 4.5:1 contrast.

