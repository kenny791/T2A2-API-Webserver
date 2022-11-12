from flask import Blueprint, request
from init import db, bcrypt
from models.user import User, UserSchema
from sqlalchemy.exc import IntegrityError
from datetime import timedelta
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint('auth', __name__, url_prefix="/auth")

# function to check if user is admin
def is_admin():
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    return user.is_admin

# function to check if user is original user of review/saved restaurant
def original_user():
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    return user.id

# route allows for new users to register
@auth_bp.route("/register", methods=["POST"])
def auth_register():
    try:
        data = UserSchema().load(request.json)
        user = User(
            username = data['username'],
            email = data['email'],
            password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        )
        db.session.add(user)
        db.session.commit()
        return UserSchema(exclude=['password', 'is_admin','saved', 'reviews_count', 'saved_count', 'reviews_submitted']).dump(user), 201
    except IntegrityError:
        return {'error': 'Username or email already exists'}, 409
        
# route allows for users to login
@auth_bp.route('/login/', methods=['POST'])
def auth_login():
    # Find a user by email address
    stmt = db.select(User).filter_by(email=request.json['email'])
    user = db.session.scalar(stmt)
    # If user exists and password is correct
    if user and bcrypt.check_password_hash(user.password, request.json['password']):
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
        return {'username':user.username, 'email':user.email, 'token':token}, 200
    else:
        return{'error': 'Invalid email or password'},401

# route returns all users with details
@auth_bp.route('/users/')
@jwt_required()
def get_all_users():
    if is_admin():
        stmt = db.select(User)
        users = db.session.scalars(stmt)
        return UserSchema(many=True, exclude=['password']).dump(users)
    else:
        return {'error': 'Unauthorized'}, 401


# route returns one user with details
@auth_bp.route('/users/<int:user_id>/')
@jwt_required()
def get_one_user(user_id):
    if is_admin():
        stmt = db.select(User).filter_by(id=user_id)
        user = db.session.scalar(stmt)
        if user:
            return UserSchema(exclude=['password']).dump(user)
        else:
            return {'error': 'User not found'}, 404
    else:
        return {'error': 'Unauthorized'}, 401


# route allows for admin to delete account
@auth_bp.route('/users/<int:user_id>/', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    if is_admin():
        stmt = db.select(User).filter_by(id=user_id)
        user = db.session.scalar(stmt)
        if user:
            db.session.delete(user)
            db.session.commit()
            return {'message': 'User deleted'}, 200
        else:
            return {'error': 'User not found'}, 404
    else:
        return {'error': 'Unauthorized'}, 401
