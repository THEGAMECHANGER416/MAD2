from flask_restful import Resource, Api
from flask_restful import fields, marshal
from flask_restful import reqparse
from flask import current_app as app
from flask_security import Security, SQLAlchemyUserDatastore, auth_required
from werkzeug.security import generate_password_hash
from application.data.database import db
from flask import abort
from application.data.models import User,Role,Sponsor, Influencer, Campaign, AdRequest
from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

# Signup parsers
signup_parser = reqparse.RequestParser()
signup_parser.add_argument('email', type=str, required=True, help='Email address is required')
signup_parser.add_argument('password', type=str, required=True, help='Password is required')
signup_parser.add_argument('role', type=str, required=True, choices=('Sponsor', 'Influencer', 'Admin'), help='Role is required')
signup_parser.add_argument('companyName', type=str, required=False)
signup_parser.add_argument('name', type=str, required=False)
signup_parser.add_argument('industry', type=str, required=False)
signup_parser.add_argument('budget', type=int, required=False)
signup_parser.add_argument('category', type=str, required=False)
signup_parser.add_argument('niche', type=str, required=False)
signup_parser.add_argument('reach', type=int, required=False)

# Output fields
sponsor_fields = {
    'companyName': fields.String,
    'industry': fields.String,
    'budget': fields.Integer,
    'isVerified': fields.Boolean
}

influencer_fields = {
    'name': fields.String,
    'category': fields.String,
    'niche': fields.String,
    'reach': fields.Integer
}

user_fields = {
    'id': fields.Integer,
    'email': fields.String,
    'role': fields.String(attribute=lambda x: x.role.name if x.role else None),
    'sponsor': fields.Nested(sponsor_fields, allow_null=True),
    'influencer': fields.Nested(influencer_fields, allow_null=True)
}

class SignupAPI(Resource):
    def post(self):
        args = signup_parser.parse_args()

        existing_user = User.query.filter_by(email=args['email']).first()
        if existing_user:
            return {'msg': 'User with this email already exists'}, 409

        role_name = args['role']
        role = Role.query.filter_by(name=role_name).first()
        if not role:
            return {'msg': 'Invalid role provided'}, 400

        if role_name == 'Sponsor':
            if not args['companyName'] or not args['industry'] or args['budget'] is None:
                return {'msg': 'Company name, industry, and budget are required for sponsor role'}, 400
            
            new_user = User(email=args['email'], role=role)
            new_user.set_password(args['password'])

            db.session.add(new_user)
            db.session.commit()

            new_sponsor = Sponsor(
                user_id=new_user.id,
                company_name=args['companyName'],
                industry=args['industry'],
                budget=args['budget']
            )
            db.session.add(new_sponsor)
            new_user.sponsor = new_sponsor
        elif role_name == 'Influencer':
            if not args['category'] or not args['niche'] or not args['name'] or args['reach'] is None:
                return {'msg': 'Category, niche, name and reach are required for influencer role'}, 400
            
            new_user = User(email=args['email'], role=role)
            new_user.set_password(args['password'])

            db.session.add(new_user)
            db.session.commit()

            new_influencer = Influencer(
                user_id=new_user.id,
                name=args['name'],
                category=args['category'],
                niche=args['niche'],
                reach=args['reach']
            )
            db.session.add(new_influencer)
            new_user.influencer = new_influencer
        db.session.commit()
        access_token = create_access_token(identity=new_user.id)
        return {'msg':'User Created Successfully','access_token': access_token},201


# Login Parser
login_parser = reqparse.RequestParser()
login_parser.add_argument('email', type=str, required=True, help='Email address is required')
login_parser.add_argument('password', type=str, required=True, help='Password is required')

class LoginAPI(Resource):
    def post(self):
        args = login_parser.parse_args()
        user = User.query.filter_by(email=args['email']).first()

        if user and user.check_password(args['password']):
            access_token = create_access_token(identity=user.id)
            return {'msg':'Login Successfull','access_token': access_token},200
        else:
            return {'msg': 'Invalid email or password'}, 401


# Request parsers
update_profile_parser = reqparse.RequestParser()
update_profile_parser.add_argument('email', type=str, required=False)
update_profile_parser.add_argument('password', type=str, required=False)
update_profile_parser.add_argument('company_name', type=str, required=False)
update_profile_parser.add_argument('industry', type=str, required=False)
update_profile_parser.add_argument('budget', type=int, required=False)
update_profile_parser.add_argument('name', type=str, required=False)
update_profile_parser.add_argument('category', type=str, required=False)
update_profile_parser.add_argument('niche', type=str, required=False)
update_profile_parser.add_argument('reach', type=int, required=False)

class ProfileAPI(Resource):
    @jwt_required()
    @marshal_with(user_fields)
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if user.role.name == 'Sponsor':
            sponsor = Sponsor.query.filter_by(user_id=user.id).first()
            user.sponsor = sponsor

        elif user.role.name == 'Influencer':
            influencer = Influencer.query.filter_by(user_id=user.id).first()
            user.influencer = influencer

        return user, 200

    @jwt_required()
    def put(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return {'message': 'User not found'}, 404
        
        args = update_profile_parser.parse_args()

        if args['email']:
            user.email = args['email']
        
        if args['password']:
            user.set_password(args['password'])

        if user.role.name == 'sponsor':
            sponsor = Sponsor.query.filter_by(user_id=user.id).first()
            if sponsor:
                if args['company_name']:
                    sponsor.company_name = args['company_name']
                if args['industry']:
                    sponsor.industry = args['industry']
                if args['budget'] is not None:
                    sponsor.budget = args['budget']
        elif user.role.name == 'influencer':
            influencer = Influencer.query.filter_by(user_id=user.id).first()
            if influencer:
                if args['name']:
                    influencer.name = args['name']
                if args['category']:
                    influencer.category = args['category']
                if args['niche']:
                    influencer.niche = args['niche']
                if args['reach'] is not None:
                    influencer.reach = args['reach']

        db.session.commit()
        return {'message': 'Profile updated successfully'}, 200