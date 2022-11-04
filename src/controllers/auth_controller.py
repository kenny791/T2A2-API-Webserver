from flask import Blueprint, request
from init import db, bcrypt
from models.user import User, UserSchema
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__, url_prefix="/auth")

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
        
# @auth.route("/login", methods=["POST"])
# def auth_login():
#     # get the user data from the request
#     user_fields = user_schema.load(request.json)
#     #find the user in the database by email
#     user = User.query.filter_by(email=user_fields["email"]).first()
#     # there is not a user with that email or if the password is no correct send an error
#     if not user or not bcrypt.check_password_hash(user.password, user_fields["password"]):
#         return abort(401, description="Incorrect username and password")
    
#     #create a variable that sets an expiry date
#     expiry = timedelta(days=1)
#     #create the access token
#     access_token = create_access_token(identity=str(user.id), expires_delta=expiry)
#     # return the user email and the access token
#     return jsonify({"user":user.email, "token": access_token })