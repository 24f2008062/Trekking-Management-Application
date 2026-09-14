# 🏔️ LEVEL 2 - VIVA PREPARATION & CODE WALKTHROUGH GUIDE

> **Note:** All answers are written in very simple, easy-to-understand language without complex technical jargon for quick learning and viva confidence!

---

## 🏗️ SECTION 1: Project / Architecture

### 1. What does your app do? Explain your app and the idea behind it.
* **Idea:** Managing trekking trips manually on paper or spreadsheets is confusing for trekking companies. It is hard to keep track of remaining seats, assign guides to trips, and manage customer bookings.
* **What the App Does:** It is a **Trekking Management System** that automates the whole process. It supports 3 user roles:
  1. **Admin:** Manages treks, approves guides/staff, views all bookings, and blocks bad users.
  2. **Staff (Guides):** Manages their assigned treks and updates available seat counts.
  3. **Trekkers (Customers):** Search for treks, book trip slots, and view or cancel bookings.

---

### 2. Explain what you have done in your project.
* I built a full-stack web application using **Flask (Python)** and **SQLite database**.
* Created database models for Users, Roles, Treks, Bookings, and Profiles.
* Written backend routes for registration, login, staff approval, trek CRUD operations, slot management, and search.
* Designed responsive HTML dashboards using **Bootstrap 5** and **Jinja2** templates.

---

### 3. Explain the code structure of your project.
* `app.py` ──► Backend Python server containing all routes and control logic.
* `models.py` ──► Database models, table schemas, and table relationships.
* `templates/` ──► Folder containing HTML pages (dashboards, forms, login page).
* `static/css/style.css` ──► Custom styling for layout and navigation.
* `instance/app.db` ──► SQLite database file storing persistent data.
* `create-admin.py` ──► Initializer script to seed default admin account.

---

### 4. Explain the architecture of your application.
The application follows the **MVC (Model-View-Controller)** pattern:
* **Model:** Handled by `models.py` using SQLAlchemy (Database structure).
* **View:** Handled by HTML files in `templates/` using Jinja2 (UI seen by user).
* **Controller:** Handled by `app.py` functions using Flask routes (Business logic).

---

### 5. What frameworks have you used?
1. **Flask (Python):** Backend web framework used to handle URLs, user sessions, and database queries.
2. **Bootstrap 5 (CSS):** Frontend framework used for pre-built responsive components (tables, badges, modals, buttons).

---

### 6. How does the frontend and backend work/interact?
1. User interacts with HTML forms or buttons on the **Frontend** (Browser).
2. Browser sends an **HTTP Request** (`GET` or `POST`) to the **Backend** (`app.py`).
3. Backend processes logic, talks to the **SQLite Database**, and fetches or updates data.
4. Backend renders the updated HTML page using **Jinja2** and sends it back to the Frontend.

---

### 7. Explain how your controller works — how are routes connected and how do they function?
* Routes in `app.py` use Python decorators like `@app.route('/login', methods=['GET', 'POST'])`.
* When a user visits a URL (e.g. `/login`), Flask executes the matching Python function directly below the decorator.
* The function reads input data, performs database actions, and returns either `render_template('page.html')` to show a page or `redirect('/url')` to change pages.

---

### 8. Explain any route of your choice.
Let's explain the **Login Route** (`/login`):
* Receives user's `email` and `password` via POST request.
* Queries database for user: `User.query.filter_by(email=email).first()`.
* Checks password using `bcrypt.checkpw(password, user.password)`.
* If correct, stores `user_id` in Flask `session` and redirects user to their role dashboard (`/admin-dashboard`, `/staff-dashboard`, or `/trekker-dashboard`).

---

### 9. Explain the `create_trek` route (in `app.py` named `/add-trek`).
* Protected by `@admin_required` (only admins can access).
* **GET Request:** Displays the `add_trek.html` form with a list of available staff.
* **POST Request:** Reads form values (name, location, difficulty, duration, slots, guide ID), creates a `new_trek = trek(...)` model instance, adds to database (`db.session.add`), commits changes (`db.session.commit()`), and redirects to Admin Dashboard.

---

### 10. How are you getting information in the `create_trek` route?
Information is extracted from the submitted HTML form using Flask's `request.form` dictionary:
```python
name = request.form['name']
location = request.form.get('location')
difficulty = request.form.get('difficulty', 'Moderate')
available_slots = request.form.get('available_slots', 20)
```

---

### 11. How does admin login and reach the dashboard?
1. Admin enters `admin@admin.com` and password `admin@123` on `/login`.
2. Flask checks database credentials using `bcrypt`.
3. Flask verifies that the user's role is `'admin'`.
4. Flask sets `session['user_role'] = 'admin'` and redirects to `/admin-dashboard`.
5. The `@admin_required` decorator allows access because `session['user_role'] == 'admin'`.

---

## 🗄️ SECTION 2: Models / Database

### 12. Explain your models.
In `models.py`, we have 5 main model classes:
1. `User`: Stores account info (`id`, `name`, `username`, `email`, `password`).
2. `Role`: Stores roles (`admin`, `staff`, `pending_staff`, `trekker`, `blacklisted`).
3. `trek`: Stores trek details (`name`, `location`, `difficulty`, `duration`, `available_slots`, `status`, `assigned_staff_id`).
4. `Booking`: Stores booking reservations (`trek_id`, `booking_status`, `booking_date`, `payment_status`).
5. `staff_profile`: Stores guide contact info (`user_id`, `phone`, `Address`).

---

### 13. Explain your database.
* Uses **SQLite** database (`app.db`), which is a simple file-based database.
* Managed using **Flask-SQLAlchemy** (ORM) to read and write database tables using Python objects.

---

### 14. Explain the relationships between your tables.
* **User ↔ Role:** Many-to-Many via `user_roles` junction table.
* **User ↔ staff_profile:** One-to-One (`user_id` FK with `unique=True`).
* **User (Staff) ↔ trek:** One-to-Many (`assigned_staff_id` FK in `trek` table).
* **trek ↔ Booking:** One-to-Many (`trek_id` FK in `Booking` table).
* **User (Trekker) ↔ Booking:** Many-to-Many via `user_booking` junction table.

---

### 15. How do you make a one-to-one relationship?
Place a `ForeignKey` on the child table with `unique=True` and set `uselist=False` in `db.relationship()`:
```python
profile = db.relationship("staff_profile", uselist=False, backref='user')
```

---

### 16. How do you make a one-to-many relationship?
Place a `ForeignKey` on the "Many" table and a `db.relationship()` on the "One" table:
```python
# In parent model (trek):
bookings = db.relationship('Booking', backref='trek')

# In child model (Booking):
trek_id = db.Column(db.Integer, db.ForeignKey('trek.id'))
```

---

### 17. Where have you specified that a relationship is one-to-many?
In `models.py`:
1. In `trek` model: `assigned_staff_id` FK points to `User.id` (One Staff Guide $\rightarrow$ Many Treks).
2. In `Booking` model: `trek_id` FK points to `trek.id` (One Trek $\rightarrow$ Many Bookings).

---

### 18. What is `lazy`?
`lazy` defines how related database records are loaded by SQLAlchemy:
* `lazy='select'` (Default): Loads related records only when you access the property.
* `lazy='joined'`: Loads related records immediately using a single SQL JOIN query.
* `lazy='dynamic'`: Returns a query object so you can chain further filters before fetching.

---

### 19. Explain your database schema.
The database schema consists of 5 entity tables linked together using Foreign Keys and 2 Junction tables to maintain relational data integrity.

---

### 20. What is a primary key?
A **Primary Key** is a unique identifier column (like `id`) for each row in a database table. It ensures no two rows have the same ID and cannot be NULL.

---

### 21. Is your database structured?
**Yes!** It is a **Relational Database (SQL)** structured into tables with defined columns, data types, primary keys, and foreign keys.

---

### 22. Explain the database structure/schema.
It contains:
* `user`: Primary user details.
* `role` & `user_roles`: Multi-role assignment.
* `trek`: Trek catalog and guide assignment.
* `booking` & `user_booking`: Customer booking tracking.
* `staff_profile`: Guide contact details.

---

## ⚡ SECTION 3: ORM (Object-Relational Mapping)

### 23. What is ORM?
**ORM** stands for **Object-Relational Mapping**. It is a technique that lets you interact with database tables using Python objects and code instead of writing raw SQL commands (`SELECT`, `INSERT`, `UPDATE`).

---

### 24. Which ORM have you used?
**Flask-SQLAlchemy** (which is a Flask wrapper for SQLAlchemy in Python).

---

### 25. Have you used ORM in your project?
**Yes!** Every database action in the project uses ORM syntax like:
* Fetching: `User.query.all()`
* Inserting: `db.session.add(new_trek)`
* Committing: `db.session.commit()`

---

## 🔄 SECTION 4: CRUD Operations

### 26. What is CRUD?
CRUD stands for the 4 core database operations:
* **C**reate (Insert new data)
* **R**ead (Query/Fetch data)
* **U**pdate (Modify existing data)
* **D**elete (Remove data)

---

### 27. Show where you have used CRUD in your code.
In `app.py`:
* **Create:** `db.session.add(new_trek)` in `/add-trek` route.
* **Read:** `trek.query.all()` in `/admin-dashboard` route.
* **Update:** `curr_trek.status = request.form['status']` and `db.session.commit()` in `/edit-trek` route.
* **Delete:** `db.session.delete(del_trek)` in `/delete-trek` route.

---

## 📈 SECTION 5: Scaling

### 28. What is scaling?
Scaling means expanding your application's hardware or infrastructure capacity so it can handle more user traffic without slowing down or crashing.

---

### 29. What is vertical scaling?
**Vertical Scaling (Scaling UP):** Adding more hardware power (more RAM, faster CPU, bigger SSD) to your **single existing server**.

---

### 30. What is horizontal scaling?
**Horizontal Scaling (Scaling OUT):** Adding **more server machines** to run copies of your application together using a Load Balancer.

---

### 31. Explain the difference between vertical and horizontal scaling.
| Feature | Vertical Scaling (Scaling UP) | Horizontal Scaling (Scaling OUT) |
| :--- | :--- | :--- |
| **Method** | Upgrade existing single machine | Add more server machines |
| **Hardware Limit** | Limited by single machine hardware capacity | Virtually unlimited capacity |
| **Downtime** | Requires server restart during upgrade | Zero downtime (load balancer shifts traffic) |

---

## 🌐 SECTION 6: HTTP Protocol & Methods

### 32. What are HTTP methods?
HTTP methods tell the server what action to perform:
* **`GET`:** Used to retrieve/read data from the server (e.g. loading a page).
* **`POST`:** Used to submit new data to the server (e.g. submitting a form).
* **`PUT` / `PATCH`:** Used to update existing data on the server.
* **`DELETE`:** Used to remove data from the server.

---

### 33. Explain HTTP status codes.
Status codes are 3-digit numbers returned by the server to show the result of a request:
* `2xx` = Success (e.g. `200 OK`)
* `3xx` = Redirection (e.g. `302 Found`)
* `4xx` = Client Error (e.g. `404 Not Found`, `401 Unauthorized`)
* `5xx` = Server Error (e.g. `500 Internal Server Error`)

---

### 34. Explain some HTTP status codes in detail.
* **`200 OK`:** Request succeeded and data is returned normally.
* **`302 Found (Redirect)`:** Server temporarily redirects browser to another URL (e.g. after login).
* **`404 Not Found`:** The requested URL page or resource does not exist on the server.
* **`500 Internal Server Error`:** The server encountered an unexpected error or python code crashed.

---

## 🎨 SECTION 7: CSS & Frontend Styling

### 35. Which CSS have you used?
I have used **Custom CSS** (`static/css/style.css`) along with **Bootstrap 5** framework.

---

### 36. What CSS-related things have you used in your project?
* **Bootstrap Grid System** (`row`, `col-md-6`) for page layout.
* **Bootstrap Components:** Navigation bars, card components, badges, forms, buttons, responsive tables, and tabbed navigation.
* **Custom CSS:** Background styling, sidebar layout, and custom padding/margins.

---

### 37. What is the priority/order between inline, internal and external CSS?
1. **Highest Priority:** Inline CSS (`<h1 style="color:red;">`)
2. **Second Priority:** Internal CSS (`<style>` tag inside HTML head)
3. **Lowest Priority:** External CSS (`<link rel="stylesheet" href="style.css">`)

---

### 38. Which type of CSS is more useful for a large project?
**External CSS!** Because it separates design from HTML logic, allows reusability across hundreds of pages, caches in the user's browser for speed, and simplifies code maintenance.

---

## 📝 SECTION 8: Jinja & HTML Templates

### 39. Where have you used Jinja?
In all HTML files under the `templates/` folder to dynamically output variables (`{{ user.name }}`) and write template logic (`{% if %}`, `{% for %}`).

---

### 40. What is template inheritance?
Template inheritance allows you to create a master "base" layout HTML file (`base.html`) with header, footer, and navbar, and let child HTML pages inherit it (`{% extends 'base.html' %}`) so you don't repeat code.

---

### 41. Show where you have used template inheritance.
At the top of `admin_dashboard.html`:
```jinja2
{% extends 'base.html' %}

{% block content %}
  <!-- Admin Dashboard Page Content Here -->
{% endblock %}
```

---

### 42. Write a Jinja loop for a list where the marks should be greater than 40.
```jinja2
<ul>
  {% for student in students %}
    {% if student.marks > 40 %}
      <li>{{ student.name }} - Marks: {{ student.marks }}</li>
    {% endif %}
  {% endfor %}
</ul>
```

---

## 🛠️ SECTION 9: Practical Code Changes (Viva Demo Tasks)

### 43. Run the application and demonstrate it.
Run command in terminal:
```bash
python app.py
```
Open browser at `http://127.0.0.1:5000`.

---

### 44. Make changes to the code.
Open `app.py` or HTML templates, modify text/logic, save file, and refresh browser.

---

### 45. Add an age field to the registration page.
In `templates/register.html`:
```html
<div class="mb-3">
    <label for="age" class="form-label">Age</label>
    <input type="number" class="form-control" id="age" name="age" placeholder="Enter your age" required>
</div>
```

---

### 46. Add a condition that age must be greater than 18 and less than 100.
In `app.py` inside `register()` route:
```python
age = request.form.get('age')
if age:
    age_val = int(age)
    if age_val <= 18 or age_val >= 100:
        return render_template('register.html', error="Age must be greater than 18 and less than 100.")
```

---

### 47. Write a route to fetch a user ID from the database.
```python
@app.route('/user/<int:user_id>')
def get_user_details(user_id):
    user = User.query.get_or_404(user_id)
    return f"User Found: ID={user.id}, Name={user.name}, Email={user.email}"
```

---

## 🎯 SECTION 10: Project Demonstration & Viva Tasks

### 48. Demonstrate your project.
1. Show `/login` screen.
2. Log in as Admin (`admin@admin.com`).
3. Show Admin Dashboard (Treks table, Guide assignments, Staff approvals).
4. Log out and log in as Trekker.

---

### 49. Demonstrate the core functionalities of your application.
* **Trek Creation:** Add a new trek from Admin Panel.
* **Staff Assignment:** Assign guide to trek.
* **Booking:** Book trek slot as Trekker (shows slot count decreasing by 1).
* **Cancellation:** Cancel trek as Trekker (shows slot count increasing by 1).

---

### 50. Register/login as a user, book a trek and update the user profile.
1. Open `/register`, select **Trekker**, fill details, and submit.
2. Log in at `/login`.
3. On Trekker Dashboard, search for an open trek and click **Book Now**.
4. Click **Update Profile**, change name/email, and click **Save**.

---

## 🆔 SECTION 11: Verification / Initial Steps

### 51. Show your ID card.
Present your official student identity card to the interviewer.

### 52. Show your GitHub repository and collaborator.
Open your project repository on GitHub in browser, showing commits, commit history, and team collaborators.

### 53. Download the project / perform checksum.
Run git clone or run hash checksum command:
```bash
sha256sum app.py
```
This prints the unique hash code verifying file contents.
