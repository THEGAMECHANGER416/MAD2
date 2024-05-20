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