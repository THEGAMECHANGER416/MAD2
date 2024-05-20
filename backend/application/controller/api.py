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

# Request parsers
signup_parser = reqparse.RequestParser()
signup_parser.add_argument('email', type=str, required=True, help='Email address is required')
signup_parser.add_argument('password', type=str, required=True, help='Password is required')
signup_parser.add_argument('role', type=str, required=True, choices=('Sponsor', 'Influencer', 'Admin'), help='Role is required')
signup_parser.add_argument('company_name', type=str, required=False)
signup_parser.add_argument('industry', type=str, required=False)
signup_parser.add_argument('budget', type=int, required=False)
signup_parser.add_argument('category', type=str, required=False)
signup_parser.add_argument('niche', type=str, required=False)
signup_parser.add_argument('reach', type=int, required=False)

login_parser = reqparse.RequestParser()
login_parser.add_argument('email', type=str, required=True, help='Email address is required')
login_parser.add_argument('password', type=str, required=True, help='Password is required')

# Output fields
user_fields = {
    'id': fields.Integer,
    'email': fields.String,
    'role': fields.String(attribute=lambda x: x.role.name if x.role else None)
}

class SignupAPI(Resource):
    @marshal_with(user_fields)
    def post(self):
        args = signup_parser.parse_args()

        # Check if the role provided is valid
        role_name = args['role']
        role = Role.query.filter_by(name=role_name).first()
        if not role:
            return {'message': 'Invalid role provided'}, 400

        # Create a new user instance
        new_user = User(
            email=args['email'],
            role=role
        )
        new_user.set_password(args['password'])

        db.session.add(new_user)
        db.session.commit()

        # Assign the specific role
        if role_name == 'Sponsor':
            if not args['company_name'] or not args['industry'] or args['budget'] is None:
                return {'message': 'Company name, industry, and budget are required for sponsor role'}, 400

            new_sponsor = Sponsor(
                user_id=new_user.id,
                company_name=args['company_name'],
                industry=args['industry'],
                budget=args['budget']
            )
            db.session.add(new_sponsor)
        elif role_name == 'Influencer':
            if not args['category'] or not args['niche'] or args['reach'] is None:
                return {'message': 'Category, niche, and reach are required for influencer role'}, 400

            new_influencer = Influencer(
                user_id=new_user.id,
                category=args['category'],
                niche=args['niche'],
                reach=args['reach']
            )
            db.session.add(new_influencer)

        db.session.commit()

        return new_user, 201

class LoginAPI(Resource):
    def post(self):
        args = login_parser.parse_args()

        user = User.query.filter_by(email=args['email']).first()

        if user and user.check_password(args['password']):
            access_token = create_access_token(identity=user.id)
            return {'access_token': access_token}, 200
        else:
            return {'message': 'Invalid email or password'}, 401

class ProfileAPI(Resource):
    @jwt_required()
    @marshal_with(user_fields)
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        return user, 200