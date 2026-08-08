from traceback import print_tb
from app import *
from models import User, db, Role


with app.app_context():

    admin_role = Role.query.filter_by(rolename='admin').first()

    if not admin_role:
        admin_role = Role(rolename='admin')
        db.session.add(admin_role)
        db.session.commit()

    admin = User.query.filter(
        User.role.any(Role.rolename=='admin')).first()
    if not admin:
        admin = User(
            name = 'admin',
            username = 'admin',
            email = 'admin@admin.com',
            password =hash_password('admin@123'),
        )
        admin.role.append(admin_role)
        db.session.add(admin)
        db.session.commit()
        print('admin created successfully')
    else:
        print("admin user already exists")


