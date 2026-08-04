from flask import url_for
import bcrypt
from os import readinto
from flask import Flask, render_template, request, redirect, session
from functools import wraps
from flask_sqlalchemy import SQLAlchemy  
from flask_migrate import Migrate
from models import db, User, staff_profile,Role, trek, Booking
import bcrypt

app = Flask(__name__)
app.secret_key = "super_secret_trek_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
db.init_app(app)
migrate = Migrate(app, db)

import models


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('user_role') != 'admin':
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

# Password hashing

def hash_password(pasword):

    pass_bytes = pasword.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pass_bytes, salt)

@app.route('/')
def home():

    return redirect('/login')

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
        all_user = all_users
    ) 




@app.route('/add-trek', methods=['GET', 'POST'])
@admin_required
def add_trek():


    if request.method == 'POST':
        name = request.form['name']
        difficulty = request.form.get('difficulty','Moderate')
        duration = request.form['duration']
        available_slots = request.form.get('available_slots', 20)
        status = request.form.get('status','Moderate')
        assigned_staff_id = request.form.get('assigned_staff_id')
        new_trek = trek(
            name = name,
            difficulty = difficulty,
            duration = duration,
            available_slots = available_slots,
            status = status,
            assigned_staff_id = int(assigned_staff_id) if assigned_staff_id else None
        )
        db.session.add(new_trek)
        db.session.commit()
        return redirect(url_for('admin_dashboard', tab='manage-treks'))
    staff = User.query.filter(User.role.any(Role.rolename == 'staff')).all()
    return render_template('add_trek.html', staff=staff)

@app.route('/edit-trek/<int:trek_id>', methods=['GET', 'POST'])
@admin_required
def edit_trek(trek_id):


    curr_trek = trek.query.get_or_404(trek_id)
    if request.method == 'POST':

        curr_trek.name = request.form['name']
        curr_trek.difficulty = request.form.get('difficulty', 'Moderate')
        curr_trek.duration = request.form['duration']
        curr_trek.available_slots = request.form.get('available_slots', 20)
        curr_trek.status = request.form.get('status', 'Moderate')
        assigned_staff_id = request.form.get('assigned_staff_id')
        curr_trek.assigned_staff_id = int(assigned_staff_id) if assigned_staff_id else None
        db.session.commit()
        return redirect(url_for('admin_dashboard', tab='manage-treks'))


    staff = User.query.filter(User.role.any(Role.rolename == 'staff')).all()
    return render_template('edit_trek.html', trek=curr_trek, staff=staff)



@app.route('/delete-trek/<int:trek_id>', methods=['GET','POST'])
@admin_required
def delete_trek(trek_id):


    if request.method=='POST':
        del_trek = trek.query.filter_by(id = trek_id).first()
        db.session.delete(del_trek)
        db.session.commit()
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
    return redirect(url_for('admin_dashboard', tab='manage-staff'))


@app.route('/approve-staff/<int:user_id>', methods = ['POST'])
@admin_required
def approve_staff(user_id):


    user = User.query.get_or_404(user_id)
    pending_role = Role.query.filter_by(rolename = 'pending_staff').first()
    staff_role = Role.query.filter_by(rolename = 'staff').first()

    if pending_role in user.role:
        user.role.remove(pending_role)
    if staff_role not in user.role:
        user.role.append(staff_role)
    db.session.commit()
    return redirect(url_for('admin_dashboard', tab='manage-staff'))



@app.route('/blacklist/<int:user_id>', methods=['POST'])
@admin_required
def blacklist_user(user_id):
    user = User.query.get_or_404(user_id)

    # Get or create the blacklisted role
    blacklisted_role = Role.query.filter_by(rolename='blacklisted').first()
    if not blacklisted_role:
        blacklisted_role = Role(rolename='blacklisted')
        db.session.add(blacklisted_role)

    # Remove all current roles and assign blacklisted role
    user.role.clear()
    user.role.append(blacklisted_role)
    db.session.commit()

    return redirect(url_for('admin_dashboard', tab='manage-user'))


@app.route('/unblacklist/<int:user_id>', methods=['POST'])
@admin_required
def unblacklist_user(user_id):
    user = User.query.get_or_404(user_id)
    blacklisted_role = Role.query.filter_by(rolename='blacklisted').first()

    if blacklisted_role and blacklisted_role in user.role:
        user.role.remove(blacklisted_role)

    # Restore role as staff if profile exists, otherwise as trekker
    restored_rolename = 'staff' if user.profile else 'trekker'
    restored_role = Role.query.filter_by(rolename=restored_rolename).first()
    if not restored_role:
        restored_role = Role(rolename=restored_rolename)
        db.session.add(restored_role)

    if restored_role not in user.role:
        user.role.append(restored_role)

    db.session.commit()
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
        return redirect(url_for('admin_dashboard', tab='manage-staff'))
    all_treks = trek.query.all()
    return render_template('assign_staff.html', staff_member=staff_member, treks=all_treks)




@app.route('/staff-dashboard')
def staff_dashboard():

    return render_template('staff_dashboard.html')




@app.route('/trekker-dashboard')
def trekker_dashboard():

    return render_template('trekker_dashboard.html')




@app.route('/login', methods = ['GET','POST'])
def login():


    if request.method=="POST":
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        
        if user and bcrypt.checkpw(
            password.encode('utf-8'), 
            user.password
        ):    
            session['user_id'] = user.id
            if any(role.rolename == 'admin' for role in user.role):
                session['user_role'] = 'admin'
                return redirect('/admin-dashboard')
            
            elif any(role.rolename == 'staff' for role in user.role):
                session['user_role'] = 'staff'
                return redirect('/staff-dashboard')

            elif any(role.rolename == 'pending_staff' for role in user.role):
                
                return render_template('login.html', error="Your staff registration is pending admin approval.")
            
            else:
                session['user_role'] = 'trekker'
                return redirect('/trekker-dashboard')
        else:
            return render_template('login.html', error = "Invalid email or password")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/register', methods=['GET','POST'])
def register():


    if request.method=='POST':
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        selected_role = request.form.get('role', 'trekker')

        existing_email = User.query.filter_by(email=email).first()
        existing_username = User.query.filter_by(username=username).first()

        if existing_email or existing_username:
            # Return an error message to the user instead of crashing
            return render_template('register.html', error="Email or Username already exists.")


        hashed_password = hash_password(password)

        role_to_assing = 'pending_staff' if selected_role == 'staff' else selected_role

        role = Role.query.filter_by(rolename=role_to_assing).first()
        if not role:
            role = Role(
                rolename=role_to_assing
            )
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
        
        return redirect('/login')
    return render_template('register.html')

@app.route('/complete-staff-profile/<int:user_id>', methods=['GET', 'POST'])
def complete_staff_profile(user_id):


    if request.method == 'POST':
        phone = int(request.form['phone'])
        address = request.form['address']

        profile = staff_profile(
            user_id=user_id,
            phone=phone,
            Address=address
        )
        db.session.add(profile)
        db.session.commit() 

        return redirect('/login')
    return render_template('staff_details.html', user_id=user_id)


@app.route('/search', methods=['GET','POST'])
@admin_required
def search():
    all_treks = trek.query.all()
    all_staffs = User.query.filter(User.role.any(Role.rolename == 'staff')).all()
    pending_staff = User.query.filter(User.role.any(Role.rolename == 'pending_staff')).all()
    all_bookings = Booking.query.all()
    all_users = User.query.all()
    blacklisted_users = User.query.filter(User.role.any(Role.rolename == 'blacklisted')).all()

    search_query = request.form.get('search', '')
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

if __name__ == "__main__":
    app.run(debug=True)