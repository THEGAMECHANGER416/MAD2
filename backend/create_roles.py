from application.data.models import User, Role, db

def create_roles():
    admin = Role(id=1, name='Admin')
    sponsor = Role(id=2, name='Sponsor')
    influencer = Role(id=3, name='Influencer')

    db.session.add(admin)
    db.session.add(sponsor)
    db.session.add(influencer)

    db.session.commit()
    print("Roles created successfully!")

def create_admin():
    admin = User(id=1, email='admin@brandly.com', role_id=1)
    admin.set_password('admin@123')
    db.session.add(admin)
    db.session.commit()
    print("Admin created successfully!")