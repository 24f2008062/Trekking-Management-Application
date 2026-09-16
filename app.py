import os
import json
import time
import logging
from datetime import date
from functools import wraps
from contextlib import contextmanager

from flask import Flask, render_template, request, redirect, session, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import event
from sqlalchemy.engine import Engine
import bcrypt

from models import db, User, staff_profile, Role, trek, Booking, Trek, StaffProfile

# ==============================================================================
# LOGGING & INITIALIZATION
# ==============================================================================
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("trekking.enterprise")

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "super_secret_trek_key_1919_weimar")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

raw_db_url = os.environ.get("DATABASE_URL")
if raw_db_url:
    if raw_db_url.startswith("postgres://"):
        raw_db_url = raw_db_url.replace("postgres://", "postgresql://", 1)
    app.config["SQLALCHEMY_DATABASE_URI"] = raw_db_url
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# ==============================================================================
# SQLITE ENTERPRISE PRAGMA TUNING (WAL MODE & BUSY TIMEOUT)
# ==============================================================================
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Tuning SQLite for high concurrency, concurrent reads, and write lock wait."""
    try:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL;")
        cursor.execute("PRAGMA busy_timeout=5000;")
        cursor.execute("PRAGMA synchronous=NORMAL;")
        cursor.execute("PRAGMA temp_store=MEMORY;")
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()
    except Exception as e:
        logger.warning(f"Could not apply SQLite WAL PRAGMAs: {e}")

db.init_app(app)
migrate = Migrate(app, db)

# ==============================================================================
# RESILIENT REDIS CACHING ENGINE WITH GRACEFUL FALLBACK
# ==============================================================================
class ResilientCache:
    """Enterprise multi-tier cache with transparent fallback if Redis is offline."""
    def __init__(self, host='localhost', port=6379, db=1):
        self.client = None
        self.is_connected = False
        try:
            import redis
            self.client = redis.Redis(
                host=host, 
                port=port, 
                db=db, 
                decode_responses=True, 
                socket_timeout=0.4, 
                socket_connect_timeout=0.4
            )
            redis_url = os.environ.get("REDIS_URL")
            if redis_url:
                self.client = redis.from_url(
                    redis_url,
                    decode_responses=True,
                    socket_timeout=0.5,
                    socket_connect_timeout=0.5
                )
            else:
                self.client = redis.Redis(
                    host=host, 
                    port=port, 
                    db=db, 
                    decode_responses=True, 
                    socket_timeout=0.4, 
                    socket_connect_timeout=0.4
                )
            self.client.ping()
            self.is_connected = True
            logger.info("Enterprise Redis Cache connected (DB 1).")
            logger.info("Enterprise Redis Cache connected.")
        except Exception as e:
            logger.warning(f"Redis Cache offline; falling back to relational queries: {e}")
            self.client = None
            self.is_connected = False

    def get(self, key):
        if not self.is_connected or not self.client:
            return None
        try:
            val = self.client.get(key)
            return json.loads(val) if val else None
        except Exception:
            return None

    def set(self, key, value, timeout=3600):
        if not self.is_connected or not self.client:
            return
        try:
            self.client.setex(key, timeout, json.dumps(value))
        except Exception:
            pass

    def invalidate(self, pattern):
        if not self.is_connected or not self.client:
            return
        try:
            keys = self.client.keys(pattern)
            if keys:
                self.client.delete(*keys)
        except Exception:
            pass

cache = ResilientCache()

# ==============================================================================
# DISTRIBUTED MUTEX LOCKING FOR CONCURRENCY SAFETY
# ==============================================================================
@contextmanager
def acquire_slot_lock(trek_id, timeout=2.0):
    """Prevents race conditions on slot reservations using atomic Redis locking."""
    lock_acquired = False
    lock_key = f"mutex:trek_slot:{trek_id}"
    token = f"tok_{time.time()}"
    client = cache.client if cache.is_connected else None

    if client:
        start_t = time.time()
        while time.time() - start_t < timeout:
            if client.set(lock_key, token, nx=True, ex=3):
                lock_acquired = True
                break
            time.sleep(0.02)

    try:
        yield lock_acquired
    finally:
        if client and lock_acquired:
            try:
                lua = """
                    if redis.call('get', KEYS[1]) == ARGV[1] then
                        return redis.call('del', KEYS[1])
                    else
                        return 0
                    end
                """
                client.eval(lua, 1, lock_key, token)
            except Exception:
                pass

# ==============================================================================
# SERVER-SIDE SESSION & RATE LIMITING DEFENSE
# ==============================================================================
try:
    if cache.is_connected:
        import redis
        from flask_session import Session
        redis_url = os.environ.get("REDIS_URL")
        app.config["SESSION_TYPE"] = "redis"
        app.config["SESSION_REDIS"] = redis.Redis(host='localhost', port=6379, db=0)
        if redis_url:
            app.config["SESSION_REDIS"] = redis.from_url(redis_url)
        else:
            app.config["SESSION_REDIS"] = redis.Redis(host='localhost', port=6379, db=0)
        app.config["SESSION_USE_SIGNER"] = True
        app.config["PERMANENT_SESSION_LIFETIME"] = 86400
        Session(app)
        logger.info("Server-side Redis Session Storage active (DB 0).")
        logger.info("Server-side Redis Session Storage active.")
except Exception as e:
    logger.info(f"Standard session retained: {e}")

try:
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address
    storage_uri = "redis://localhost:6379/2" if cache.is_connected else "memory://"
    redis_url = os.environ.get("REDIS_URL")
    if cache.is_connected:
        storage_uri = redis_url if redis_url else "redis://localhost:6379/2"
    else:
        storage_uri = "memory://"
    limiter = Limiter(
        get_remote_address,
        app=app,
        storage_uri=storage_uri,
        default_limits=["1000 per hour", "150 per minute"]
    )
except Exception:
    class NoOpLimiter:
        def limit(self, *args, **kwargs):
            def decorator(f):
                return f
            return decorator
    limiter = NoOpLimiter()

# ==============================================================================
# SECURITY HEADERS (ZERO-TRUST PERIMETER)
# ==============================================================================
@app.after_request
def set_enterprise_security_headers(response):
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Permissions-Policy'] = 'camera=(), microphone=(), geolocation=()'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "font-src 'self' https://fonts.gstatic.com https://cdn.jsdelivr.net data:; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdn.jsdelivr.net; "
        "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
        "img-src 'self' data: https:; "
        "frame-ancestors 'none';"
    )
    return response

# ==============================================================================
# AUTHENTICATION & ACCESS CONTROL HELPERS
# ==============================================================================
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('user_role') != 'admin':
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

def hash_password(password):
    pass_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(pass_bytes, salt)

# ==============================================================================
# OBSERVABILITY & HEALTH PROBES
# ==============================================================================
@app.route('/healthz')
def health_liveness():
    """Liveness probe: verifies WSGI process execution."""
    return jsonify({"status": "alive", "service": "trekking-management", "timestamp": time.time()}), 200

@app.route('/readyz')
def health_readiness():
    """Readiness probe: validates database and Redis backends."""
    checks = {"database": False, "redis": cache.is_connected}
    try:
        db.session.execute(db.text("SELECT 1"))
        checks["database"] = True
    except Exception as e:
        logger.error(f"Readiness DB Failure: {e}")

    status_code = 200 if checks["database"] else 503
    return jsonify({"status": "ready" if checks["database"] else "degraded", "checks": checks}), status_code

# ==============================================================================
# PUBLIC & AUTHENTICATION ROUTES
# ==============================================================================
@app.route('/')
def home():
    if 'user_id' in session:
        role = session.get('user_role')
        if role == 'admin':
            return redirect('/admin-dashboard')
        elif role == 'staff':
            return redirect('/staff-dashboard')
        else:
            return redirect('/trekker-dashboard')
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def login():
    if request.method == "POST":
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.checkpw(password.encode('utf-8'), user.password):
            # Check for blacklisted role
            if any(role.rolename == 'blacklisted' for role in user.role):
                return render_template('login.html', error="Your account has been sanctioned. Access denied.")

            session['user_id'] = user.id

            if any(role.rolename == 'admin' for role in user.role):
                session['user_role'] = 'admin'
                return redirect('/admin-dashboard')
            elif any(role.rolename == 'staff' for role in user.role):
                session['user_role'] = 'staff'
                return redirect('/staff-dashboard')
            elif any(role.rolename == 'pending_staff' for role in user.role):
                session.clear()
                return render_template('login.html', error="Your staff registration is pending admin approval.")
            else:
                session['user_role'] = 'trekker'
                return redirect('/trekker-dashboard')
        else:
            return render_template('login.html', error="Invalid email address or password.")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
@limiter.limit("3 per hour")
def register():
    if request.method == 'POST':
        name = request.form['name'].strip()
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password']
        selected_role = request.form.get('role', 'trekker')

        if User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first():
            return render_template('register.html', error="Email or Username is already registered.")

        hashed_password = hash_password(password)
        role_to_assign = 'pending_staff' if selected_role == 'staff' else selected_role

        role = Role.query.filter_by(rolename=role_to_assign).first()
        if not role:
            role = Role(rolename=role_to_assign)
            db.session.add(role)
            db.session.commit()

        user = User(
            name=name,
            username=username,
            email=email,
            password=hashed_password
        )
        db.session.add(user)
        user.role.append(role)
        db.session.commit()

        if selected_role == 'staff':
            return redirect(f'/complete-staff-profile/{user.id}')

        flash("Account created successfully. Please authenticate.")
        return redirect('/login')

    return render_template('register.html')

@app.route('/complete-staff-profile/<int:user_id>', methods=['GET', 'POST'])
def complete_staff_profile(user_id):
    if request.method == 'POST':
        phone = request.form.get('phone', '').strip()
        address = request.form.get('address', '').strip()

        if not phone.isdigit() or len(phone) > 10:
            return render_template('staff_details.html', user_id=user_id, error="Phone number must be a valid 10-digit number.")

        profile = staff_profile(
            user_id=user_id,
            phone=int(phone),
            Address=address
        )
        db.session.add(profile)
        db.session.commit()

        flash("Staff dossier submitted. Awaiting administrative approval.")
        return redirect('/login')

    return render_template('staff_details.html', user_id=user_id)

# ==============================================================================
# TREKKER ROUTES & DIGITAL PASS
# ==============================================================================
@app.route('/trekker-dashboard')
def trekker_dashboard():
    if 'user_id' not in session:
        return redirect('/login')

    active_tab = request.args.get('tab', 'book-treks')
    user_id = session.get('user_id')
    current_user = User.query.get(user_id)

    if not current_user:
        session.clear()
        return redirect('/login')

    treks = trek.query.all()
    my_treks = current_user.booking
    active_bookings = [b for b in my_treks if b.trek and b.trek.status not in ['Completed', 'Closed']]
    trekking_history = [b for b in my_treks if b.trek and b.trek.status in ['Completed']]

    return render_template(
        'trekker_dashboard.html',
        active_tab=active_tab,
        current_user=current_user,
        available_treks=treks,
        my_treks=my_treks,
        trekking_history=trekking_history,
        active_bookings=active_bookings
    )

@app.route('/trekker-search', methods=['GET', 'POST'])
def trekker_search():
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session.get('user_id')
    current_user = User.query.get(user_id)
    treks = trek.query.all()
    my_treks = current_user.booking if current_user else []

    search_query = request.form.get('search', '').strip()
    location_filter = request.form.get('location', '').strip()
    difficulty_filter = request.form.get('difficulty', '').strip()

    query = trek.query
    if search_query:
        query = query.filter(trek.name.ilike(f"%{search_query}%"))
    if location_filter:
        query = query.filter(trek.location.ilike(f"%{location_filter}%"))
    if difficulty_filter:
        query = query.filter(trek.difficulty == difficulty_filter)

    search_treks = query.all() if (search_query or location_filter or difficulty_filter) else []

    return render_template(
        'trekker_dashboard.html',
        active_tab='search',
        search_query=search_query,
        location_filter=location_filter,
        difficulty_filter=difficulty_filter,
        search_treks=search_treks,
        current_user=current_user,
        available_treks=treks,
        my_treks=my_treks
    )

@app.route('/book-trek/<trek_id>', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
def book_trek(trek_id):
    if 'user_id' not in session:
        return redirect('/login')

    current_trek = trek.query.get_or_404(trek_id)
    user_id = session.get('user_id')
    current_user = User.query.get_or_404(user_id)

    if current_trek.status in ['Closed', 'Completed']:
        flash("This expedition is closed for booking.")
        return redirect('/trekker-dashboard')

    if current_trek.available_slots <= 0:
        flash("All slots for this expedition are completely booked.")
        return redirect('/trekker-dashboard')

    if request.method == 'POST':
        # Concurrency safety: acquire atomic slot lock to prevent double booking
        with acquire_slot_lock(trek_id):
            # Re-verify slot availability under lock
            db.session.refresh(current_trek)
            if current_trek.available_slots <= 0:
                flash("The last slot was just claimed by another explorer. Expedition full.")
                return redirect('/trekker-dashboard')

            booking = Booking(
                trek_id=trek_id,
                booking_status='Confirm',
                booking_date=date.today(),
                payment_status='Confirm'
            )
            current_trek.available_slots -= 1
            current_user.booking.append(booking)
            db.session.add(booking)
            db.session.commit()

            # Cache invalidation
            cache.invalidate("trek:*")
            flash("Reservation confirmed! Your official expedition permit has been generated.")
            return redirect(url_for('trek_pass', booking_id=booking.id))

    return render_template('book_trek.html', trek=current_trek, current_user=current_user)

@app.route('/cancel-booking/<booking_id>', methods=['GET', 'POST'])
def cancel_booking(booking_id):
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session.get('user_id')
    current_user = User.query.get_or_404(user_id)
    current_booking = Booking.query.get_or_404(booking_id)

    # IDOR Security Check: Only the booking owner or admin can cancel
    is_admin = session.get('user_role') == 'admin'
    if not is_admin and current_booking not in current_user.booking:
        flash("Security violation: You can only cancel your own bookings.")
        return redirect(url_for('trekker_dashboard', tab='my-treks'))

    if request.method == 'POST':
        with acquire_slot_lock(current_booking.trek_id):
            current_booking.booking_status = 'Cancelled'
            current_booking.payment_status = 'Refunded'
            if current_booking in current_user.booking:
                current_user.booking.remove(current_booking)
            if current_booking.trek:
                current_booking.trek.available_slots += 1
            db.session.commit()
            cache.invalidate("trek:*")
            flash("Booking cancelled and refund processed.")

        if is_admin:
            return redirect(url_for('admin_dashboard', tab='manage-booking'))
        return redirect(url_for('trekker_dashboard', tab='my-treks'))

    return redirect(url_for('admin_dashboard' if is_admin else 'trekker_dashboard'))

@app.route('/trek-pass/<int:booking_id>')
def trek_pass(booking_id):
    """Render high-contrast printable Bauhaus Digital Trek Pass."""
    if 'user_id' not in session:
        return redirect('/login')

    booking = Booking.query.get_or_404(booking_id)
    user_id = session.get('user_id')
    user_role = session.get('user_role')

    # Authorization verification
    if user_role not in ['admin', 'staff'] and booking.user:
        if booking.user[0].id != user_id:
            flash("Unauthorized: You do not have permission to view this pass.")
            return redirect(url_for('trekker_dashboard'))

    trekker = booking.user[0] if booking.user else User.query.get(user_id)
    return render_template('trek_pass.html', booking=booking, trekker=trekker)

@app.route('/update-trekker-profile', methods=['GET', 'POST'])
def update_trekker_profile():
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session.get('user_id')
    current_user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        current_user.name = request.form['name'].strip()
        current_user.email = request.form['email'].strip()
        db.session.commit()
        flash("Profile updated successfully.")
        return redirect(url_for('trekker_dashboard', tab='profile'))

    return render_template('update_trekker_profile.html', current_user=current_user)

# ==============================================================================
# STAFF (ALPINE GUIDE) ROUTES
# ==============================================================================
@app.route('/staff-dashboard')
def staff_dashboard():
    if 'user_id' not in session:
        return redirect('/login')

    active_tab = request.args.get('tab', 'dashboard')
    user_id = session.get('user_id')
    current_user = User.query.get_or_404(user_id)

    assigned_treks = trek.query.filter(trek.assigned_staff_id == user_id).all()
    assigned_trek_ids = [t.id for t in assigned_treks]
    assigned_bookings = Booking.query.filter(Booking.trek_id.in_(assigned_trek_ids)).all() if assigned_trek_ids else []

    return render_template(
        'staff_dashboard.html',
        active_tab=active_tab,
        current_user=current_user,
        assigned_treks=assigned_treks,
        assinged_bookings=assigned_bookings
    )

@app.route("/edit-staff-trek/<int:trek_id>", methods=['GET', 'POST'])
def edit_staff_trek(trek_id):
    if 'user_id' not in session:
        return redirect('/login')

    curr_trek = trek.query.get_or_404(trek_id)

    # Guide ownership check
    if session['user_id'] != curr_trek.assigned_staff_id and session.get('user_role') != 'admin':
        flash("Unauthorized: You are not designated as the lead guide for this trail.")
        return redirect('/staff-dashboard')

    if request.method == 'POST':
        curr_trek.available_slots = int(request.form.get('available_slots', curr_trek.available_slots))
        curr_trek.status = request.form.get('status', curr_trek.status)
        db.session.commit()
        cache.invalidate("trek:*")
        flash("Trail status and slot capacity updated.")
        return redirect(url_for('staff_dashboard', tab='manage-treks'))

    return render_template('edit_staff_trek.html', trek=curr_trek)

@app.route('/update-profile', methods=['GET', 'POST'])
def update_profile():
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session.get('user_id')
    current_user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        current_user.name = request.form.get('name', current_user.name).strip()
        phone = request.form.get('phone', '').strip()
        address = request.form.get('address', '').strip()

        if phone and (not phone.isdigit() or len(phone) > 10):
            return render_template('update_profile.html', current_user=current_user, error="Phone number must not exceed 10 digits.")

        phone_val = int(phone) if phone else None

        if current_user.profile:
            current_user.profile.phone = phone_val
            current_user.profile.Address = address
        else:
            new_profile = staff_profile(user_id=current_user.id, phone=phone_val, Address=address)
            db.session.add(new_profile)

        db.session.commit()
        flash("Guide profile updated successfully.")
        return redirect(url_for('staff_dashboard', tab='profile'))

    return render_template('update_profile.html', current_user=current_user)

# ==============================================================================
# ADMIN OPERATIONS COMMAND CENTER
# ==============================================================================
@app.route('/admin-dashboard')
@admin_required
def admin_dashboard():
    active_tab = request.args.get('tab', 'dashboard')
    all_treks = trek.query.all()
    all_staffs = User.query.filter(User.role.any(Role.rolename == 'staff')).all()
    pending_staff = User.query.filter(User.role.any(Role.rolename == 'pending_staff')).all()
    all_bookings = Booking.query.all()
    all_users = User.query.all()
    blacklisted_users = User.query.filter(User.role.any(Role.rolename == 'blacklisted')).all()

    return render_template(
        'admin_dashboard.html',
        treks=all_treks,
        staff=all_staffs,
        pending_staff=pending_staff,
        bookings=all_bookings,
        blacklisted_users=blacklisted_users,
        active_tab=active_tab,
        all_user=all_users
    )

@app.route('/add-trek', methods=['GET', 'POST'])
@admin_required
def add_trek():
    if request.method == 'POST':
        name = request.form['name'].strip()
        location = request.form.get('location', '').strip()
        difficulty = request.form.get('difficulty', 'Moderate')
        duration = request.form['duration'].strip()
        available_slots = int(request.form.get('available_slots', 20))
        status = request.form.get('status', 'Open')
        assigned_staff_id = request.form.get('assigned_staff_id')

        new_trek = trek(
            name=name,
            location=location,
            difficulty=difficulty,
            duration=duration,
            available_slots=available_slots,
            status=status,
            assigned_staff_id=int(assigned_staff_id) if assigned_staff_id else None
        )
        db.session.add(new_trek)
        db.session.commit()
        cache.invalidate("trek:*")
        flash(f"Expedition '{name}' successfully provisioned.")
        return redirect(url_for('admin_dashboard', tab='manage-treks'))

    staff = User.query.filter(User.role.any(Role.rolename == 'staff')).all()
    return render_template('add_trek.html', staff=staff)

@app.route('/edit-trek/<int:trek_id>', methods=['GET', 'POST'])
@admin_required
def edit_trek(trek_id):
    curr_trek = trek.query.get_or_404(trek_id)
    if request.method == 'POST':
        curr_trek.name = request.form['name'].strip()
        curr_trek.location = request.form.get('location', '').strip()
        curr_trek.difficulty = request.form.get('difficulty', 'Moderate')
        curr_trek.duration = request.form['duration'].strip()
        curr_trek.available_slots = int(request.form.get('available_slots', 20))
        curr_trek.status = request.form.get('status', 'Open')
        assigned_staff_id = request.form.get('assigned_staff_id')
        curr_trek.assigned_staff_id = int(assigned_staff_id) if assigned_staff_id else None
        db.session.commit()
        cache.invalidate("trek:*")
        flash(f"Expedition '{curr_trek.name}' updated.")
        return redirect(url_for('admin_dashboard', tab='manage-treks'))

    staff = User.query.filter(User.role.any(Role.rolename == 'staff')).all()
    return render_template('edit_trek.html', trek=curr_trek, staff=staff)

@app.route('/delete-trek/<int:trek_id>', methods=['GET', 'POST'])
@admin_required
def delete_trek(trek_id):
    if request.method == 'POST':
        del_trek = trek.query.filter_by(id=trek_id).first()
        if del_trek:
            db.session.delete(del_trek)
            db.session.commit()
            cache.invalidate("trek:*")
            flash("Expedition deleted from catalog.")
    return redirect(url_for('admin_dashboard', tab='manage-treks'))

@app.route('/delete-staff/<int:staff_id>', methods=['GET', 'POST'])
@admin_required
def delete_staff(staff_id):
    if request.method == 'POST':
        del_staff = User.query.filter_by(id=staff_id).first()
        if del_staff:
            profile = staff_profile.query.filter_by(user_id=staff_id).first()
            if profile:
                db.session.delete(profile)
            db.session.delete(del_staff)
            db.session.commit()
            flash("Staff record removed.")
    return redirect(url_for('admin_dashboard', tab='manage-staff'))

@app.route('/approve-staff/<int:user_id>', methods=['POST'])
@admin_required
def approve_staff(user_id):
    user = User.query.get_or_404(user_id)
    pending_role = Role.query.filter_by(rolename='pending_staff').first()
    staff_role = Role.query.filter_by(rolename='staff').first()

    if not staff_role:
        staff_role = Role(rolename='staff')
        db.session.add(staff_role)

    if pending_role and pending_role in user.role:
        user.role.remove(pending_role)
    if staff_role not in user.role:
        user.role.append(staff_role)

    db.session.commit()
    flash(f"Guide '{user.name}' approved and granted staff privileges.")
    return redirect(url_for('admin_dashboard', tab='manage-staff'))

@app.route('/blacklist/<int:user_id>', methods=['POST'])
@admin_required
def blacklist_user(user_id):
    user = User.query.get_or_404(user_id)
    blacklisted_role = Role.query.filter_by(rolename='blacklisted').first()

    if not blacklisted_role:
        blacklisted_role = Role(rolename='blacklisted')
        db.session.add(blacklisted_role)

    user.role.clear()
    user.role.append(blacklisted_role)
    db.session.commit()

    # Instant session termination if Redis session backend is active
    if cache.is_connected and cache.client:
        try:
            keys = cache.client.keys(f"*usr_{user_id}*")
            if keys:
                cache.client.delete(*keys)
        except Exception:
            pass

    flash(f"User '{user.name}' has been sanctioned and blacklisted.")
    return redirect(url_for('admin_dashboard', tab='manage-user'))

@app.route('/unblacklist/<int:user_id>', methods=['POST'])
@admin_required
def unblacklist_user(user_id):
    user = User.query.get_or_404(user_id)
    blacklisted_role = Role.query.filter_by(rolename='blacklisted').first()

    if blacklisted_role and blacklisted_role in user.role:
        user.role.remove(blacklisted_role)

    restored_rolename = 'staff' if user.profile else 'trekker'
    restored_role = Role.query.filter_by(rolename=restored_rolename).first()
    if not restored_role:
        restored_role = Role(rolename=restored_rolename)
        db.session.add(restored_role)

    if restored_role not in user.role:
        user.role.append(restored_role)

    db.session.commit()
    flash(f"Access restored for '{user.name}' as {restored_rolename}.")
    return redirect(url_for('admin_dashboard', tab='blacklist'))

@app.route('/assign-staff/<int:staff_id>', methods=['GET', 'POST'])
@admin_required
def assign_staff(staff_id):
    staff_member = User.query.get_or_404(staff_id)
    if request.method == 'POST':
        trek_id = request.form.get('trek_id')
        if trek_id:
            selected_trek = trek.query.get_or_404(int(trek_id))
            selected_trek.assigned_staff_id = staff_member.id
            db.session.commit()
            cache.invalidate("trek:*")
            flash(f"Lead guide {staff_member.name} assigned to {selected_trek.name}.")
        return redirect(url_for('admin_dashboard', tab='manage-staff'))

    all_treks = trek.query.all()
    return render_template('assign_staff.html', staff_member=staff_member, treks=all_treks)

@app.route('/search', methods=['GET', 'POST'])
@admin_required
def search():
    all_treks = trek.query.all()
    all_staffs = User.query.filter(User.role.any(Role.rolename == 'staff')).all()
    pending_staff = User.query.filter(User.role.any(Role.rolename == 'pending_staff')).all()
    all_bookings = Booking.query.all()
    all_users = User.query.all()
    blacklisted_users = User.query.filter(User.role.any(Role.rolename == 'blacklisted')).all()

    search_query = request.form.get('search', '').strip()
    users = User.query.filter(User.name.ilike(f"%{search_query}%")).all() if search_query else []
    treks = trek.query.filter(trek.name.ilike(f"%{search_query}%")).all() if search_query else []

    return render_template(
        'admin_dashboard.html',
        active_tab='search',
        search_query=search_query,
        search_users=users,
        search_treks=treks,
        treks=all_treks,
        staff=all_staffs,
        pending_staff=pending_staff,
        bookings=all_bookings,
        blacklisted_users=blacklisted_users,
        all_user=all_users
    )

# ==============================================================================
# PRODUCTION DATABASE BOOTSTRAP & SEEDING
# ==============================================================================
def init_db_and_seed(app_instance=None):
    """Guarantees database schema, default roles, and default administrator exist."""
    target_app = app_instance or app
    with target_app.app_context():
        try:
            db.create_all()

            # Seed default system roles
            system_roles = ['admin', 'staff', 'trekker', 'pending_staff', 'blacklisted']
            for rolename in system_roles:
                existing_role = Role.query.filter_by(rolename=rolename).first()
                if not existing_role:
                    db.session.add(Role(rolename=rolename))
            db.session.commit()

            # Seed default admin user if none exists
            admin_role = Role.query.filter_by(rolename='admin').first()
            existing_admin = User.query.filter(User.role.any(Role.rolename == 'admin')).first()
            if not existing_admin and admin_role:
                admin_email = os.environ.get("ADMIN_DEFAULT_EMAIL", "admin@admin.com")
                admin_pass = os.environ.get("ADMIN_DEFAULT_PASSWORD", "admin@123")
                admin_user = User(
                    name="System Administrator",
                    username="admin",
                    email=admin_email,
                    password=hash_password(admin_pass)
                )
                admin_user.role.append(admin_role)
                db.session.add(admin_user)
                db.session.commit()
                logger.info(f"Production bootstrap: Seeded default administrator ({admin_email}).")
            else:
                logger.info("Production bootstrap: Database schema and default roles verified.")
        except Exception as e:
            logger.warning(f"Database bootstrap notice: {e}")

# Bootstrap DB & Roles upon module load
init_db_and_seed(app)

# ==============================================================================
# MAIN ENTRYPOINT
# ==============================================================================
if __name__ == "__main__":
    app.run(debug=True)
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "0").lower() in ("1", "true", "yes")
    app.run(host="0.0.0.0", port=port, debug=debug)