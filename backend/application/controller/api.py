from flask_restful import Resource, Api
from flask_restful import fields, marshal
from flask_restful import reqparse
from flask import current_app as app
from flask_security import Security, SQLAlchemyUserDatastore, auth_required
from werkzeug.security import generate_password_hash
from application.data.database import db
from application.data.models import User,Role,Sponsor, Influencer, Campaign, AdRequest
from flask import Flask, request, jsonify, abort
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import werkzeug
import datetime
from werkzeug.utils import secure_filename
import os

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
    'image': fields.String,
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

# Parsers for other models
campaign_parser = reqparse.RequestParser()
campaign_parser.add_argument('name', type=str, required=True)
campaign_parser.add_argument('description', type=str, required=True)
campaign_parser.add_argument('start_date', type=str, required=True)
campaign_parser.add_argument('end_date', type=str, required=True)
campaign_parser.add_argument('budget', type=int, required=True)
campaign_parser.add_argument('isActive', type=bool, required=True)
campaign_parser.add_argument('progress', type=int, required=True)

ad_request_parser = reqparse.RequestParser()
ad_request_parser.add_argument('campaign_id', type=int, required=True)
ad_request_parser.add_argument('influencer_id', type=int, required=False)
ad_request_parser.add_argument('requirements', type=str, required=True)
ad_request_parser.add_argument('payment_amount', type=float, required=True)
ad_request_parser.add_argument('status', type=str, required=False)
ad_request_parser.add_argument('goal', type=str, required=True)
ad_request_parser.add_argument('platform', type=str, required=True)

# Resource classes
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

        new_user = User(email=args['email'], role=role)
        new_user.set_password(args['password'])

        db.session.add(new_user)
        db.session.commit()

        if role_name == 'Sponsor':
            if not args['companyName'] or not args['industry'] or args['budget'] is None:
                return {'msg': 'Company name, industry, and budget are required for sponsor role'}, 400
            
            new_sponsor = Sponsor(
                user_id=new_user.id,
                companyName=args['companyName'],
                industry=args['industry'],
                budget=args['budget']
            )
            db.session.add(new_sponsor)
            new_user.sponsor = new_sponsor
        elif role_name == 'Influencer':
            if not args['category'] or not args['niche'] or not args['name'] or args['reach'] is None:
                return {'msg': 'Category, niche, name, and reach are required for influencer role'}, 400
            
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

        user_data = marshal(new_user, user_fields)
        return {'msg': 'User Created Successfully', 'user': user_data, 'access_token': access_token}, 201

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
            
            if user.role.name == 'Sponsor':
                sponsor = Sponsor.query.filter_by(user_id=user.id).first()
                user.sponsor = sponsor
            elif user.role.name == 'Influencer':
                influencer = Influencer.query.filter_by(user_id=user.id).first()
                user.influencer = influencer
            
            user_data = marshal(user, user_fields)
            return {'msg': 'Login Successful', 'user': user_data, 'access_token': access_token}, 200
        else:
            return {'msg': 'Invalid email or password'}, 401

# Profile Parser
update_profile_parser = reqparse.RequestParser()
update_profile_parser.add_argument('email', type=str, required=False)
update_profile_parser.add_argument('password', type=str, required=False)
update_profile_parser.add_argument('companyName', type=str, required=False)
update_profile_parser.add_argument('industry', type=str, required=False)
update_profile_parser.add_argument('image', type=werkzeug.datastructures.FileStorage, location='files')
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
            user.sponsor = Sponsor.query.filter_by(user_id=user.id).first()

        elif user.role.name == 'Influencer':
            user.influencer = Influencer.query.filter_by(user_id=user.id).first()

        return user, 200

    @jwt_required()
    @marshal_with(user_fields)
    def put(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return {'message': 'User not found'}, 404

        # Parse JSON data if present
        json_data = request.form.get('data')
        if json_data:
            args = json.loads(json_data)
        else:
            args = {}

        # Parse form data for file upload
        image_file = request.files.get('image')
        if image_file:
            args['image'] = image_file

        # Update user email and password if provided
        if args.get('email'):
            user.email = args['email']
        if args.get('password'):
            user.set_password(args['password'])

        # Handle specific fields based on role
        if user.role.name == 'Sponsor':
            sponsor = Sponsor.query.filter_by(user_id=user.id).first()
            if sponsor:
                if args.get('companyName'):
                    sponsor.companyName = args['companyName']
                if args.get('industry'):
                    sponsor.industry = args['industry']
                if args.get('budget') is not None:
                    sponsor.budget = args['budget']
        elif user.role.name == 'Influencer':
            influencer = Influencer.query.filter_by(user_id=user.id).first()
            if influencer:
                if args.get('name'):
                    influencer.name = args['name']
                if args.get('category'):
                    influencer.category = args['category']
                if args.get('niche'):
                    influencer.niche = args['niche']
                if args.get('reach') is not None:
                    influencer.reach = args['reach']

                # Handle image upload
                if image_file:
                    filename = secure_filename(image_file.filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    image_file.save(file_path)
                    print(file_path)
                    influencer.image = '/uploads/' + filename  # Save image path to database
                    print(influencer.image)

        db.session.commit()

        # Fetch the updated user and related fields to return
        updated_user = User.query.get(user_id)
        if user.role.name == 'Sponsor':
            updated_user.sponsor = Sponsor.query.filter_by(user_id=user.id).first()
        elif user.role.name == 'Influencer':
            updated_user.influencer = Influencer.query.filter_by(user_id=user.id).first()
            
        return updated_user, 200
class CampaignAPI(Resource):

    @jwt_required()
    def get(self, campaign_id=None):
        # If campaign_id is None, return all campaigns by the user
        if campaign_id is None:
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            if user.role.name == 'Sponsor':
                campaigns = Campaign.query.filter_by(sponsor_id=user_id).all()
            elif user.role.name == 'Influencer':
                campaigns = Campaign.query.filter_by(influencer_id=user_id).all()
            return [marshal(campaign, {
                'id': fields.Integer,
                'name': fields.String,
                'description': fields.String,
                'start_date': fields.DateTime,
                'end_date': fields.DateTime,
                'budget': fields.Integer,
                'isActive': fields.Boolean,
                'progress': fields.Integer,
                'sponsor_id': fields.Integer
            }) for campaign in campaigns]
        else:
            # Return a single campaign with all the associated ads
            campaign = Campaign.query.get_or_404(campaign_id)
            ads = AdRequest.query.filter_by(campaign_id=campaign_id).all()
            # Add influencer_name to each ad
            for ad in ads:
                if ad.influencer_id is not None and ad.influencer_id != 0:
                    ad.influencer_name = Influencer.query.filter_by(user_id=ad.influencer_id).first().name
                else:
                    ad.influencer_name = None
            campaign.ads = ads
            return marshal(campaign, {
                'id': fields.Integer,
                'name': fields.String,
                'description': fields.String,
                'start_date': fields.DateTime,
                'end_date': fields.DateTime,
                'budget': fields.Integer,
                'isActive': fields.Boolean,
                'progress': fields.Integer,
                'sponsor_id': fields.Integer,
                'ads': fields.List(fields.Nested({
                    'id': fields.Integer,
                    'campaign_id': fields.Integer,
                    'influencer_id': fields.Integer,
                    'requirements': fields.String,
                    'payment_amount': fields.Float,
                    'status': fields.String,
                    'goal': fields.String,
                    'platform': fields.String,
                    'influencer_name': fields.String
                }))
            })

    @jwt_required()
    def post(self):
        args = campaign_parser.parse_args()
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user.role.name != 'Sponsor':
            return {'message': 'Only sponsors can create campaigns'}, 403
        
        new_campaign = Campaign(
            name=args['name'],
            description=args['description'],
            start_date= datetime.datetime.strptime(args['start_date'], "%Y-%m-%d"),
            end_date=datetime.datetime.strptime(args['end_date'], "%Y-%m-%d"),
            budget=args['budget'],
            isActive=args['isActive'],
            progress=args['progress'],
            sponsor_id=user_id
        )
        
        db.session.add(new_campaign)
        db.session.commit()
        
        return marshal(new_campaign, {
            'id': fields.Integer,
            'name': fields.String,
            'description': fields.String,
            'start_date': fields.DateTime,
            'end_date': fields.DateTime,
            'budget': fields.Integer,
            'isActive': fields.Boolean,
            'progress': fields.Integer,
            'sponsor_id': fields.Integer
        }), 201

    @jwt_required()
    def put(self, campaign_id):
        args = campaign_parser.parse_args()
        campaign = Campaign.query.get_or_404(campaign_id)
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if user.role.name != 'Sponsor' or campaign.sponsor_id != user.id:
            return {'message': 'You do not have permission to edit this campaign'}, 403

        campaign.name = args['name']
        campaign.description = args['description']
        start_date= datetime.datetime.strptime(args['start_date'], "%Y-%m-%d"),
        end_date=datetime.datetime.strptime(args['end_date'], "%Y-%m-%d"),
        campaign.budget = args['budget']
        campaign.isActive = args['isActive']
        campaign.progress = args['progress']

        db.session.commit()
        return marshal(campaign, {
            'id': fields.Integer,
            'name': fields.String,
            'description': fields.String,
            'start_date': fields.DateTime,
            'end_date': fields.DateTime,
            'budget': fields.Integer,
            'isActive': fields.Boolean,
            'progress': fields.Integer,
            'sponsor_id': fields.Integer
        }), 200

    @jwt_required()
    def delete(self, campaign_id):
        campaign = Campaign.query.get_or_404(campaign_id)
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if user.role.name != 'Sponsor' or campaign.sponsor_id != user.id:
            return {'message': 'You do not have permission to delete this campaign'}, 403

        db.session.delete(campaign)
        db.session.commit()
        return {'message': 'Campaign Deleted Successfully'}, 204

class AdRequestAPI(Resource):
    @jwt_required()
    @marshal_with({
        'id': fields.Integer,
        'campaign_id': fields.Integer,
        'influencer_id': fields.Integer,
        'messages': fields.String,
        'requirements': fields.String,
        'payment_amount': fields.Float,
        'status': fields.String,
        'goal': fields.String,
        'platform': fields.String,
        'target_audience': fields.String,
        'budget': fields.Integer
    })
    def get(self, ad_request_id=None):
        if ad_request_id:
            ad_request = AdRequest.query.get_or_404(ad_request_id)
            return ad_request, 200
        else:
            # get ad requests where user is in influencer id or sponsor id
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            if user.role.name == 'Sponsor':
                campaigns = Campaign.query.filter_by(sponsor_id=user_id)
                ad_requests = []
                for campaign in campaigns:
                    ad_requests.extend(AdRequest.query.filter_by(campaign_id=campaign.id))
            elif user.role.name == 'Influencer':
                ad_requests = AdRequest.query.filter_by(influencer_id=user_id)
            return ad_requests

    @jwt_required()
    def post(self):
        args = ad_request_parser.parse_args()
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if user.role.name != 'Sponsor':
            return {'message': 'Only sponsors can create ad requests'}, 403

        new_ad_request = AdRequest(
            campaign_id=args['campaign_id'],
            influencer_id=args['influencer_id'],
            requirements=args['requirements'],
            payment_amount=args['payment_amount'],
            status=args['status'],
            goal=args['goal'],
            platform=args['platform']
        )

        db.session.add(new_ad_request)
        db.session.commit()

        return marshal(new_ad_request, {
            'id': fields.Integer,
            'campaign_id': fields.Integer,
            'influencer_id': fields.Integer,
            'requirements': fields.String,
            'payment_amount': fields.Float,
            'status': fields.String,
            'goal': fields.String,
            'platform': fields.String
        }), 201

    @jwt_required()
    def put(self, ad_request_id):
        args = ad_request_parser.parse_args()
        ad_request = AdRequest.query.get_or_404(ad_request_id)
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if user.role.name == 'Sponsor' and ad_request.campaign.sponsor_id != user_id:
            return {'message': 'You do not have permission to edit this ad request'}, 403

        ad_request.campaign_id = args['campaign_id']
        ad_request.influencer_id = args['influencer_id']
        ad_request.requirements = args['requirements']
        ad_request.payment_amount = args['payment_amount']
        ad_request.status = args['status']
        ad_request.goal = args['goal']
        ad_request.platform = args['platform']

        db.session.commit()
        return marshal(ad_request, {
            'id': fields.Integer,
            'campaign_id': fields.Integer,
            'influencer_id': fields.Integer,
            'platform': fields.String,
            'requirements': fields.String,
            'payment_amount': fields.Float,
            'status': fields.String,
            'goal': fields.String
        }), 200

    @jwt_required()
    def delete(self, ad_request_id):
        ad_request = AdRequest.query.get_or_404(ad_request_id)
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if user.role.name != 'Sponsor' or ad_request.campaign.sponsor_id != user_id:
            return {'message': 'You do not have permission to delete this ad request'}, 403

        db.session.delete(ad_request)
        db.session.commit()
        return '', 204

class SearchAPI(Resource):
    @jwt_required()
    def get(self):
        query = request.args.get('q')
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        results = []
        if user.role.name == 'Sponsor':
            influencers = Influencer.query.filter(Influencer.name.like(f'%{query}%'))
            print(influencers)
            return [marshal(result, {
                'id': fields.Integer,
                'name': fields.String,
                'image': fields.String,
                'category': fields.String,
                'niche': fields.String,
                'reach': fields.Integer
            }) for result in influencers], 201
        elif user.role.name == 'Influencer':
            campaigns = Campaign.query.filter(Campaign.name.like(f'%{query}%'))
            return [marshal(result, {
                'id': fields.Integer,
                'name': fields.String,
                'description': fields.String,
                'start_date': fields.DateTime,
                'end_date': fields.DateTime,
                'budget': fields.Integer,
                'isActive': fields.Boolean,
                'progress': fields.Integer
            }) for result in campaigns], 201
        return results