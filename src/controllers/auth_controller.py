from flask import Blueprint, request
from init import db, bcrypt
from models.user import User, UserSchema
from sqlalchemy.exc import IntegrityError
from datetime import timedelta
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint('auth', __name__, url_prefix="/auth")

def authorize():
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    return user.is_admin

@auth_bp.route("/register", methods=["POST"])
def auth_register():
    try:
        #Create a new User model instance from the user_info
        user = User(
            username = request.json.get('username'),
            email = request.json['email'],
            password = bcrypt.generate_password_hash(request.json['password']).decode('utf-8'),            
        )

        #Add and commit user to DB
        db.session.add(user)
        db.session.commit()
        #Respond to client
        return UserSchema(exclude=['password']).dump(user),201
    except IntegrityError:
        return {'error': 'Email address already in use'}, 409
        
@auth_bp.route('/login/', methods=['POST'])
def auth_login():
    # Find a user by email address
    stmt = db.select(User).filter_by(email=request.json['email'])
    user = db.session.scalar(stmt)
    # If user exists and password is correct
    if user and bcrypt.check_password_hash(user.password, request.json['password']):
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
        return {'email': user.email, 'token': token, 'is_admin': user.is_admin} 
    else:
        return{'error': 'Invalid email or password'},401


@auth_bp.route('/users/')
def get_all_users():
    stmt = db.select(User)
    users = db.session.scalars(stmt)
    return UserSchema(many=True, exclude=['password']).dump(users)