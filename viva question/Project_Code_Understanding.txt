===============================================================================
                   TREKKING MANAGEMENT APPLICATION
                    VIVA PREPARATION & CODE UNDERSTANDING
===============================================================================

-------------------------------------------------------------------------------
QUESTION 1: Explain your project and its problem statement.
-------------------------------------------------------------------------------
Answer:
- What is the Project?
  The Trekking Management Application is a role-based Web Application built using 
  Python (Flask framework), SQLite database (with Flask-SQLAlchemy ORM), and 
  Bootstrap 5 / HTML / CSS on the frontend.

- Problem Statement:
  Trekking agencies and adventure clubs face several operational challenges when 
  managing treks manually:
  1. Tracking available seats (slots) for upcoming trips in real time.
  2. Assigning qualified guides/staff to specific treks.
  3. Handling customer registration, bookings, and cancellations.
  4. Managing staff registration and approving guide accounts safely.
  5. Handling unruly or problematic users by blocking/blacklisting them.

- Solution Provided by this App:
  This application automates the entire trek management lifecycle. It introduces 
  Role-Based Access Control (RBAC) supporting three main user roles:
  1. Admin: System supervisor managing treks, staff approvals, and user permissions.
  2. Staff (Guides): Field guides managing assigned trek schedules and slots.
  3. Trekkers (Customers): Adventure enthusiasts discovering, filtering, booking, 
     and cancelling trek trips.

-------------------------------------------------------------------------------
QUESTION 2: Give a complete walkthrough/demo of your application.
-------------------------------------------------------------------------------
Answer:
1. Landing Page & Authentication:
   - When a user visits '/', they are automatically redirected to '/login'.
   - Unregistered users click 'Register' ('/register').

2. User Registration & Staff Onboarding:
   - Trekker Registration: Selects 'Trekker', enters details, and gets assigned 
     the 'trekker' role immediately. Redirected to login.
   - Staff Registration: Selects 'Trek Staff', enters account details, and gets 
     assigned the 'pending_staff' status. They are prompted to complete their 
     contact profile (phone number and address at '/complete-staff-profile/<user_id>'). 
     They cannot log into the staff panel until approved by an Admin.

3. Admin Panel Walkthrough ('/admin-dashboard'):
   - Dashboard Overview: Displays live counters for total treks, active guides, 
     pending approvals, total bookings, and blacklisted users.
   - Manage Treks: Admin creates new treks ('/add-trek'), edits trek attributes 
     ('/edit-trek/<id>'), or deletes treks ('/delete-trek/<id>').
   - Manage Staff & Approvals: Admin views pending staff applications and approves 
     them ('/approve-staff/<user_id>'), upgrading their role from 'pending_staff' 
     to 'staff'. Admin also assigns guides to open treks ('/assign-staff/<staff_id>').
   - User Management & Blacklist: Admin views all system users, blacklists 
     problematic accounts ('/blacklist/<user_id>'), or un-blacklists them 
     ('/unblacklist/<user_id>').
   - Global Search: Performs multi-entity search across users and treks ('/search').

4. Staff / Guide Panel Walkthrough ('/staff-dashboard'):
   - Guides log in and see treks assigned to them by the Admin.
   - Guides can update available slot counts or change trek status ('Open', 'Closed', 
     'Completed') using '/edit-staff-trek/<trek_id>'.
   - Guides view their participant roster (list of trekkers who booked their trek) 
     and update their own contact profile ('/update-profile').

5. Trekker Panel Walkthrough ('/trekker-dashboard'):
   - Trekkers log in to view available open treks.
   - Filters treks by keyword search, location, or difficulty ('Easy', 'Moderate', 'Hard') 
     via '/trekker-search'.
   - Clicks 'Book Now' ('/book-trek/<trek_id>'). The system checks slot availability, 
     decrements available slots by 1, and marks booking status as 'Confirm'.
   - Views 'My Treks' tab (active upcoming trips vs completed trekking history).
   - Cancels active bookings ('/cancel-booking/<booking_id>'), which automatically 
     restores +1 slot back to the trek and sets payment status to 'Refunded'.

-------------------------------------------------------------------------------
QUESTION 3: Explain the overall flow/data flow of your application.
-------------------------------------------------------------------------------
Answer:
1. User Action (Frontend):
   The user fills out a web form (e.g., login, book trek, add trek) or clicks an action button 
   in the browser.

2. HTTP Request Transmission:
   The browser sends a GET or POST HTTP request to a specific Flask route in 'app.py'.

3. Controller Processing & Authentication ('app.py'):
   - Flask reads incoming data from request parameters or form fields ('request.form').
   - Checks user session ('session') to verify login status.
   - Applies security rules and role decorators (e.g., '@admin_required').

4. Database Interactivity ('models.py' + SQLite 'app.db'):
   - Flask communicates with SQLite via SQLAlchemy ORM methods (e.g., 'User.query.filter_by()', 
     'db.session.add()', 'db.session.commit()').
   - Password security uses Bcrypt hashing before database persistence.

5. Response Rendering (Jinja2 Templates):
   Flask passes updated data variables to HTML templates inside the 'templates/' folder, 
   renders the final HTML, and sends it back to the user's browser.

-------------------------------------------------------------------------------
QUESTION 4: Explain your project directory/folder structure.
-------------------------------------------------------------------------------
Answer:
MAD1 PROJECT/
├── app.py                      -> Main Flask application server & route controllers.
├── models.py                   -> SQLAlchemy database schemas & entity relationships.
├── create-admin.py             -> Initializer script to seed default admin account.
├── roles.py                    -> Constant definitions for user roles.
├── requirements.txt            -> Required Python libraries (Flask, Flask-SQLAlchemy, etc.).
├── .gitignore                  -> Specifies files ignored by Git tracking.
├── instance/
│   └── app.db                  -> SQLite database file storing persistent data.
├── migrations/                 -> Database migration scripts generated by Flask-Migrate.
├── static/
│   └── css/
│       └── style.css           -> Custom CSS styles for layout, dashboards, and sidebar.
└── templates/                  -> Jinja2 HTML layout and page templates:
    ├── base.html               -> Master layout file (Navbar, Bootstrap 5 setup, Footer).
    ├── login.html              -> User login form template.
    ├── register.html           -> User registration form template.
    ├── staff_details.html      -> Staff contact details completion form.
    ├── admin_dashboard.html    -> Admin management control panel.
    ├── add_trek.html           -> Admin trek creation template.
    ├── edit_trek.html          -> Admin trek editing template.
    ├── assign_staff.html       -> Guide-to-trek assignment template.
    ├── staff_dashboard.html    -> Guide/Staff portal template.
    ├── edit_staff_trek.html    -> Staff trek status update template.
    ├── update_profile.html     -> Staff profile edit page.
    ├── trekker_dashboard.html  -> Customer portal & trek search page.
    ├── book_trek.html          -> Trek reservation confirmation page.
    └── update_trekker_profile.html -> Trekker profile edit page.

-------------------------------------------------------------------------------
QUESTION 5: Explain the purpose of each major file in your project.
-------------------------------------------------------------------------------
Answer:
- 'app.py': The core application controller. Sets up Flask app config, secret key, 
  database URI, authentication decorators, route handlers for all endpoints, business 
  logic, and template rendering.
- 'models.py': Defines database tables using SQLAlchemy ORM (User, Role, trek, Booking, 
  staff_profile, user_roles, user_booking) and establishes relationships like foreign keys.
- 'templates/base.html': Master HTML layout template containing Bootstrap 5 links, CSS, 
  top navbar, flash message container, and Jinja '{% block content %}' placeholder for child templates.
- 'create-admin.py': Command-line utility script that creates the default admin user account 
  ('admin@admin.com' with hashed password 'admin@123') in the database on initial setup.
- 'requirements.txt': List of Python packages required to run the project. Used with 
  'pip install -r requirements.txt'.

-------------------------------------------------------------------------------
QUESTION 6: Explain your `models.py`.
-------------------------------------------------------------------------------
Answer:
'models.py' defines the database architecture using SQLAlchemy ORM. It contains 5 main entities 
and 2 junction tables:

1. 'User' Model: Stores user credentials (id, name, username, email, password). Linked to 
   roles via 'user_roles', staff profile via 1-to-1, bookings via 'user_booking', and 
   assigned treks via foreign key.
2. 'Role' Model: Stores role names (id, rolename). Contains role definitions ('admin', 
   'staff', 'pending_staff', 'trekker', 'blacklisted').
3. 'user_roles' (Junction Table): Association table mapping User to Role (Many-to-Many).
4. 'trek' Model: Stores trek catalog items (id, name, location, difficulty, duration, 
   available_slots, assigned_staff_id, status).
5. 'Booking' Model: Stores reservation records (id, trek_id, booking_status, booking_date, 
   payment_status).
6. 'user_booking' (Junction Table): Association table mapping User to Booking (Many-to-Many).
7. 'staff_profile' Model: Stores extended profile info for staff members (id, user_id, 
   phone, Address).

-------------------------------------------------------------------------------
QUESTION 7: Explain your routes/controllers.
-------------------------------------------------------------------------------
Answer:
Routes in 'app.py' act as HTTP request handlers (controllers). They receive requests from 
the browser, execute logic, query database models, and return HTTP responses:

- Authentication Routes:
  - GET/POST '/login': Authenticates credentials and stores session state.
  - GET '/logout': Clears session data.
  - GET/POST '/register': Registers new trekker or staff account.
  - GET/POST '/complete-staff-profile/<user_id>': Collects staff phone and address.

- Admin Routes (Protected by '@admin_required'):
  - GET '/admin-dashboard': Displays admin metrics, trek table, staff approvals, bookings.
  - GET/POST '/add-trek': Creates a new trek catalog item.
  - GET/POST '/edit-trek/<trek_id>': Updates existing trek details or reassigns guide.
  - POST '/delete-trek/<trek_id>': Deletes a trek record.
  - POST '/approve-staff/<user_id>': Upgrades 'pending_staff' role to 'staff'.
  - POST '/blacklist/<user_id>': Revokes user roles and assigns 'blacklisted'.
  - POST '/unblacklist/<user_id>': Restores user access.
  - GET/POST '/assign-staff/<staff_id>': Assigns staff member to a selected trek.
  - GET/POST '/search': Executes global search across users and treks.

- Staff Routes:
  - GET '/staff-dashboard': Displays assigned treks and booked participants.
  - GET/POST '/edit-staff-trek/<trek_id>': Allows guide to update slots or trek status.
  - GET/POST '/update-profile': Updates staff contact information.

- Trekker Routes:
  - GET '/trekker-dashboard': Main portal showing open treks and active bookings.
  - GET/POST '/trekker-search': Filters treks by keyword, location, or difficulty.
  - GET/POST '/book-trek/<trek_id>': Reserves trek slot and creates booking record.
  - GET/POST '/cancel-booking/<booking_id>': Cancels booking and restores slot count.

-------------------------------------------------------------------------------
QUESTION 8: Explain one important route/function in detail.
-------------------------------------------------------------------------------
Answer:
Let's analyze the 'book_trek(trek_id)' route function in detail:

Function Code & Logic:
1. Endpoint & Access: Defined at '@app.route("/book-trek/<trek_id>", methods=["GET", "POST"])'.
2. Parameter Retrieval:
   - Receives 'trek_id' from URL path.
   - Fetches logged-in user ID from session ('session.get("user_id")').
   - Queries 'current_trek = trek.query.get(trek_id)' and 'current_user = User.query.get(user_id)'.
3. Validation Checks:
   - Check 1: If 'current_trek.status' is 'Closed' or 'Completed', flashes "This trek is closed." 
     and redirects user back to dashboard.
   - Check 2: If 'current_trek.available_slots <= 0', flashes "All slots for this trek is full." 
     and redirects user back.
4. Booking Processing (POST Request):
   - Initializes a new 'Booking' object:
     - trek_id = trek_id
     - booking_status = 'Confirm'
     - booking_date = date.today()
     - payment_status = 'Confirm'
   - Decrements trek slot inventory: 'current_trek.available_slots -= 1'.
   - Connects booking to user: 'current_user.booking.append(booking)'.
   - Persists changes: 'db.session.add(booking)' and 'db.session.commit()'.
   - Redirects trekker back to '/trekker-dashboard?tab=book-treks'.

-------------------------------------------------------------------------------
QUESTION 9: Explain how the login flow works.
-------------------------------------------------------------------------------
Answer:
1. User visits '/login' (GET request) -> Flask renders 'login.html' form.
2. User submits email and password -> Browser sends POST request to '/login'.
3. Backend lookup:
   - Flask queries database: 'user = User.query.filter_by(email=email).first()'.
4. Password verification:
   - Uses 'bcrypt.checkpw(password.encode("utf-8"), user.password)'.
5. Role determination & Session assignment:
   - If credentials match, Flask sets 'session["user_id"] = user.id'.
   - Role checks:
     - Admin role -> set 'session["user_role"] = "admin"', redirect to '/admin-dashboard'.
     - Staff role -> set 'session["user_role"] = "staff"', redirect to '/staff-dashboard'.
     - Pending staff role -> render login page with error "Your staff registration is pending admin approval."
     - Trekker role -> set 'session["user_role"] = "trekker"', redirect to '/trekker-dashboard'.
6. Invalid Login Handling:
   - If user does not exist or password check fails, renders 'login.html' with error message 
     "Invalid email or password".

-------------------------------------------------------------------------------
QUESTION 10: Explain how data flows from frontend → backend → database → frontend.
-------------------------------------------------------------------------------
Answer:
Let's follow data flow during the "Add New Trek" feature:

1. Frontend (View Layer):
   - Admin opens '/add-trek' form in browser.
   - Inputs trek name ("Himalayan Expedition"), location ("Manali"), difficulty ("Hard"), 
     duration ("5 Days"), available slots (25), status ("Open"), and assigned staff.
   - Clicks "Submit" button.

2. Backend (Controller Layer):
   - Browser sends POST request with form payload to Flask route '/add-trek'.
   - Flask route reads form data using 'request.form['name']', 'request.form['location']', etc.

3. Database (Model / Persistence Layer):
   - Flask constructs SQLAlchemy model object: 'new_trek = trek(name=..., location=..., ...)'.
   - Adds to session: 'db.session.add(new_trek)'.
   - Commits transaction: 'db.session.commit()'.
   - SQLite executes 'INSERT INTO trek (...)' and generates a new primary key ID.

4. Backend to Frontend Response:
   - Flask executes 'redirect(url_for("admin_dashboard", tab="manage-treks"))'.
   - 'admin_dashboard' route fetches updated list: 'all_treks = trek.query.all()'.
   - Renders 'admin_dashboard.html' with Jinja template passing 'treks=all_treks'.
   - Browser receives updated HTML showing the new trek in the management table.

-------------------------------------------------------------------------------
QUESTION 11: Explain the logic behind your major features.
-------------------------------------------------------------------------------
Answer:
1. Slot Inventory Auto-Management:
   - When a trekker books a slot, 'available_slots' decreases by 1.
   - When a trekker cancels a booking, 'available_slots' increases by 1.
   - Prevents overbooking by blocking booking requests when 'available_slots <= 0'.

2. Two-Step Staff Approval Lifecycle:
   - Prevents unauthorized access to staff guide controls.
   - Step 1: Staff user registers and is assigned 'pending_staff' role.
   - Step 2: Staff completes phone and address profile.
   - Step 3: Admin reviews application on admin dashboard and clicks 'Approve', upgrading 
     role to 'staff'.

3. Access Revocation & Blacklisting System:
   - Allows admin to block abusive users.
   - Blacklisting clears user's existing roles and appends 'blacklisted'.
   - When un-blacklisted, the system checks if a staff profile exists—if yes, restores 'staff' 
     role; otherwise restores 'trekker' role.

4. Multi-Criteria Trek Discovery & Filtering:
   - Trekkers filter open treks using keyword search, location matching, and difficulty levels.
   - Utilizes SQL case-insensitive search ('ilike') for flexible query matching.

-------------------------------------------------------------------------------
QUESTION 12: Why did you choose the particular technologies/libraries used in your project?
-------------------------------------------------------------------------------
Answer:
1. Python & Flask:
   - Flask is lightweight, easy to structure, and ideal for building production-grade MVC web apps.
   - Provides full control over routing, session handling, and database integration.

2. Flask-SQLAlchemy (ORM):
   - Abstract raw SQL into Python objects, preventing SQL injection vulnerabilities and 
     speeding up development.

3. SQLite:
   - File-based, serverless database embedded directly in Python. Requires zero external database 
     server configuration during development.

4. Bcrypt:
   - Industrial-standard password hashing algorithm. Uses automatic salt generation to prevent 
     rainbow table attacks and credential leaks.

5. Bootstrap 5 & Jinja2:
   - Bootstrap 5 provides mobile-responsive layout grids, navbars, modals, and tabbed panels.
   - Jinja2 provides dynamic server-side HTML rendering with template inheritance.

-------------------------------------------------------------------------------
QUESTION 13: What challenges did you face while building the project?
-------------------------------------------------------------------------------
Answer:
1. Multi-Role Authorization & Route Security:
   - Ensuring users cannot access endpoints outside their privilege level (e.g. preventing 
     trekkers from accessing '/admin-dashboard'). Solved by creating custom decorator '@admin_required' 
     and session role checks.

2. Slot Synchronization on Cancellation:
   - Maintaining accurate slot counts when bookings are created or cancelled, ensuring slots count 
     never drops below 0 or desynchronizes with booking records.

3. Staff Profile & Onboarding Lifecycle:
   - Designing the pending approval pipeline where staff accounts stay locked in 'pending_staff' 
     until admin verification.

4. Complex Foreign Key & Junction Relationships:
   - Managing Many-to-Many relationships ('user_roles', 'user_booking') alongside 1-to-1 ('staff_profile') 
     and 1-to-Many ('trek.assigned_staff_id') relations in SQLAlchemy without causing circular reference issues.

-------------------------------------------------------------------------------
QUESTION 14: What would you improve if you had more time?
-------------------------------------------------------------------------------
Answer:
1. Real Online Payment Gateway Integration:
   - Integrate Stripe or Razorpay API to process real credit/debit card payments instead of simulated status.

2. Automated Email & SMS Alerts:
   - Use Flask-Mail or Twilio to send automated booking confirmation emails and trek reminder notifications.

3. Trek Reviews & Rating System:
   - Allow trekkers to post star ratings and reviews for completed treks and assigned guides.

4. PDF Booking Receipt Export:
   - Add a feature allowing trekkers to download printable PDF booking passes.

5. Live Weather Forecast Integration:
   - Fetch real-time weather forecasts for trek locations using an external weather API.

-------------------------------------------------------------------------------
QUESTION 15: Explain something you implemented and why you implemented it that way.
-------------------------------------------------------------------------------
Answer:
- Implementation: Custom Python Decorator '@admin_required'.

- Code:
  def admin_required(f):
      @wraps(f)
      def decorated_function(*args, **kwargs):
          if 'user_id' not in session or session.get('user_role') != 'admin':
              return redirect('/login')
          return f(*args, **kwargs)
      return decorated_function

- Why Implemented This Way:
  Instead of duplicating session check logic ('if "user_id" not in session or session.get("user_role") != "admin": return redirect("/login")') 
  inside every single admin controller function, I created a reusable decorator function.

- Advantage:
  It follows the DRY (Don't Repeat Yourself) principle. Adding '@admin_required' above any route 
  automatically secures it, making code maintainable, readable, and secure.

-------------------------------------------------------------------------------
QUESTION 16: Explain a functionality from your project line-by-line.
-------------------------------------------------------------------------------
Answer:
Let's explain the 'approve_staff' functionality line-by-line:

Line 1:  @app.route('/approve-staff/<int:user_id>', methods=['POST'])
         -> Registers a Flask POST route accepting the staff member's user_id from the URL.

Line 2:  @admin_required
         -> Security decorator verifying that the current user is logged in as an Admin.

Line 3:  def approve_staff(user_id):
         -> Defines controller function receiving user_id argument.

Line 4:      user = User.query.get_or_404(user_id)
         -> Fetches User object from database by primary key user_id; throws 404 error if not found.

Line 5:      pending_role = Role.query.filter_by(rolename='pending_staff').first()
         -> Queries database for the 'pending_staff' Role object.

Line 6:      staff_role = Role.query.filter_by(rolename='staff').first()
         -> Queries database for the approved 'staff' Role object.

Line 7:      if not staff_role:
         -> Checks if the 'staff' role exists in the Role table.

Line 8:          staff_role = Role(rolename='staff')
         -> Creates new 'staff' Role object if it doesn't exist yet.

Line 9:          db.session.add(staff_role)
         -> Stages new role object creation in database session.

Line 10:     if pending_role and pending_role in user.role:
         -> Checks if user currently has the 'pending_staff' role assigned.

Line 11:         user.role.remove(pending_role)
         -> Removes 'pending_staff' role from user's assigned roles list.

Line 12:     if staff_role not in user.role:
         -> Checks if user does not yet have the active 'staff' role.

Line 13:         user.role.append(staff_role)
         -> Adds 'staff' role to user's assigned roles list.

Line 14:     db.session.commit()
         -> Commits transaction to SQLite database, updating roles permanently.

Line 15:     return redirect(url_for('admin_dashboard', tab='manage-staff'))
         -> Redirects admin browser back to staff management tab on admin dashboard.

-------------------------------------------------------------------------------
QUESTION 17: Explain your ER diagram/database schema.
-------------------------------------------------------------------------------
Answer:
The ER Diagram consists of 5 main entities and 2 junction tables:

Entities & Junctions:
1. USER (Attributes: id, name, username, email, password)
2. ROLE (Attributes: id, rolename)
3. USER_ROLES (Junction: user_id FK, role_id FK)
4. STAFF_PROFILE (Attributes: id, user_id FK UNIQUE, phone, Address)
5. TREK (Attributes: id, name, location, difficulty, duration, available_slots, assigned_staff_id FK, status)
6. BOOKING (Attributes: id, trek_id FK, booking_status, booking_date, payment_status)
7. USER_BOOKING (Junction: user_id FK, booking_id FK)

Visual ER Diagram Mapping:
[ USER ] ── (Many-to-Many via USER_ROLES) ──► [ ROLE ]
[ USER ] ── (One-to-One) ───────────────────► [ STAFF_PROFILE ]
[ USER ] ── (One-to-Many as Guide) ─────────► [ TREK ]
[ TREK ] ── (One-to-Many) ──────────────────► [ BOOKING ]
[ USER ] ── (Many-to-Many via USER_BOOKING) ─► [ BOOKING ]

-------------------------------------------------------------------------------
QUESTION 18: Explain every table, column and constraint in your database.
-------------------------------------------------------------------------------
Answer:
1. 'User' Table:
   - 'id': INTEGER, Primary Key, Auto-Increment. Unique user identity.
   - 'name': VARCHAR(200), NOT NULL. Full name of user.
   - 'username': VARCHAR(200), NOT NULL, UNIQUE constraint. Unique handle.
   - 'email': VARCHAR(200), NOT NULL, UNIQUE constraint. Unique email address.
   - 'password': VARCHAR(300), NOT NULL. Hashed bcrypt password string.

2. 'Role' Table:
   - 'id': INTEGER, Primary Key, Auto-Increment. Unique role identity.
   - 'rolename': VARCHAR(200), NOT NULL, UNIQUE constraint. Role name string 
     ('admin', 'staff', 'pending_staff', 'trekker', 'blacklisted').

3. 'user_roles' Table (Junction Table):
   - 'user_id': Foreign Key referencing 'user.id', Primary Key component.
   - 'role_id': Foreign Key referencing 'role.id', Primary Key component.

4. 'trek' Table:
   - 'id': INTEGER, Primary Key, Auto-Increment. Unique trek identity.
   - 'name': VARCHAR(200), NOT NULL. Trek name.
   - 'location': VARCHAR(200), Nullable. Location description.
   - 'difficulty': VARCHAR(200), NOT NULL. Difficulty level ('Easy', 'Moderate', 'Hard').
   - 'duration': VARCHAR(200). Duration string (e.g. "4 Days").
   - 'available_slots': INTEGER. Remaining slot count available for booking.
   - 'assigned_staff_id': Foreign Key referencing 'user.id', Nullable. ID of assigned guide.
   - 'status': VARCHAR(200). Status string ('Open', 'Closed', 'Completed').

5. 'Booking' Table:
   - 'id': INTEGER, Primary Key, Auto-Increment. Unique booking identity.
   - 'trek_id': Foreign Key referencing 'trek.id'. ID of booked trek.
   - 'booking_status': VARCHAR(200), NOT NULL. Reservation state ('Confirm', 'Cancelled').
   - 'booking_date': DATE, NOT NULL. Date when booking was made.
   - 'payment_status': VARCHAR(200). Payment state ('Confirm', 'Refunded').

6. 'user_booking' Table (Junction Table):
   - 'user_id': Foreign Key referencing 'user.id', Primary Key component.
   - 'booking_id': Foreign Key referencing 'booking.id', Primary Key component.

7. 'staff_profile' Table:
   - 'id': INTEGER, Primary Key, Auto-Increment. Profile identity.
   - 'user_id': Foreign Key referencing 'user.id', NOT NULL, UNIQUE constraint (enforces 1-to-1 relationship).
   - 'phone': BIGINT / INTEGER. Contact phone number.
   - 'Address': VARCHAR(200), NOT NULL. Residence address.

-------------------------------------------------------------------------------
QUESTION 19: Explain the relationship between your database tables.
-------------------------------------------------------------------------------
Answer:
1. User <-> Role (Many-to-Many):
   - Defined via 'user_roles' junction table.
   - A user can be assigned roles, and a role can be assigned to multiple users.

2. User <-> staff_profile (One-to-One):
   - 'staff_profile.user_id' is a Foreign Key referencing 'User.id' with a UNIQUE constraint.
   - Each staff member has exactly one contact profile, and each profile belongs to one user.

3. User (Staff/Guide) <-> trek (One-to-Many):
   - 'trek.assigned_staff_id' is a Foreign Key referencing 'User.id'.
   - A staff member can guide multiple treks over time, but each trek has one designated guide.

4. trek <-> Booking (One-to-Many):
   - 'Booking.trek_id' is a Foreign Key referencing 'trek.id'.
   - A trek can have multiple customer bookings, but each booking belongs to one specific trek.

5. User (Trekker) <-> Booking (Many-to-Many):
   - Defined via 'user_booking' junction table.
   - A trekker can make multiple bookings, and a booking record is linked back to the trekker user.

-------------------------------------------------------------------------------
QUESTION 20: Explain how a particular feature is implemented across frontend, backend and database.
-------------------------------------------------------------------------------
Answer:
Feature Selected: Trek Discovery & Search Feature across Frontend, Backend, and Database.

1. Frontend (HTML Form & UI):
   - Location: 'templates/trekker_dashboard.html'
   - UI Component: A search filter form containing:
     - Input field named 'search' for keyword entry.
     - Form input named 'location' for location keyword.
     - Dropdown select named 'difficulty' ('Easy', 'Moderate', 'Hard').
   - Action: Submitting form sends HTTP POST request to '/trekker-search'.

2. Backend (Flask Controller in 'app.py'):
   - Controller Function: 'trekker_search()'
   - Processing steps:
     - Extracts search parameters: 'search_query = request.form.get("search", "").strip()'
     - Initializes SQLAlchemy query: 'query = trek.query'
     - Dynamically attaches SQL filter conditions:
       - 'if search_query: query = query.filter(trek.name.ilike(f"%{search_query}%"))'
       - 'if location_filter: query = query.filter(trek.location.ilike(f"%{location_filter}%"))'
       - 'if difficulty_filter: query = query.filter(trek.difficulty == difficulty_filter)'
     - Executes query: 'search_treks = query.all()'.
     - Passes 'search_treks' list to 'trekker_dashboard.html' via 'render_template()'.

3. Database (SQLite Execution):
   - SQLite receives compiled SQL statement generated by SQLAlchemy ORM:
     'SELECT * FROM trek WHERE name LIKE '%keyword%' AND location LIKE '%loc%' AND difficulty = 'Moderate''
   - Database scans table indexes and returns matching record rows to Flask.

4. Frontend Rendering:
   - Jinja2 loops over matching items: '{% for trek in search_treks %}'
   - Renders matching trek cards displaying trek name, location badge, difficulty badge, 
     available slots, duration, assigned guide name, and 'Book Now' button.
===============================================================================
