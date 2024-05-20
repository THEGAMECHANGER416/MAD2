from .database import db
from flask_security import UserMixin, RoleMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(255))

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password_hash = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship('Role', backref=db.backref('users', lazy='dynamic'))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Sponsor(db.Model):
    __tablename__ = 'sponsor'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    company_name = db.Column(db.String(100))
    industry = db.Column(db.String(100))
    budget = db.Column(db.Integer)
    isVerified = db.Column(db.Boolean())
    campaigns = db.relationship('Campaign', backref='sponsor',lazy=True)

class Influencer(db.Model):
    __tablename__ = 'influencer'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False,unique=True)
    name = db.Column(db.String(100))
    category = db.Column(db.String(100))
    niche = db.Column(db.String(100))
    reach = db.Column(db.Integer)
    ad_requests = db.relationship('AdRequest', backref='influencer',lazy=True)

class Campaign(db.Model):
    __tablename__ = 'campaign'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    budget = db.Column(db.Integer)
    isActive = db.Column(db.Boolean)
    isPrivate = db.Column(db.Boolean)

    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsor.id'),nullable=False)
    ads = db.relationship('AdRequest', backref='campaign',lazy=True)

class AdRequest(db.Model):
    __tablename__ = 'ad_request'
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'),nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencer.id'),nullable=True)
    messages = db.Column(db.Text)
    requirements = db.Column(db.Text)
    payment_amount = db.Column(db.Float)
    status = db.Column(db.String(50))

