from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError
from datetime import date, timedelta
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity


app = Flask(__name__)
app.config ['JSON_SORT_KEYS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://db_dev:password123@127.0.0.1:5432/food_finder'
app.config['JWT_SECRET_KEY'] = 'hello there'


db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

#creates table
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    is_admin = db.Column(db.Boolean(), default=False)

class Restaurant(db.Model):
    __tablename__ ='restaurants'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(),nullable=False)
    address = db.Column(db.String())
    is_vegan = db.Column(db.Boolean())
    price_range = db.Column(db.String())


class RestaurantSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'address', 'is_vegan', 'price_range')
        ordered = True

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'email', 'password', 'is_admin')
        ordered = True



def authorize():
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    return user.is_admin



#Defining a custom CLI (terminal) command
@app.cli.command('create')
def create_db():
    db.create_all()
    print("Tables created")



#adds entity
@app.cli.command('seed')
def seed_db():
    users = [
        User(
            username = 'admin',
            email = 'admin@email.com',
            password = bcrypt.generate_password_hash('password123').decode('utf-8'),
            is_admin = True
        ),
        User(
            username = 'user1',
            email = 'user1@email.com',
            password = bcrypt.generate_password_hash('password123').decode('utf-8')
        ),
        User(
            username = 'user2',
            email = 'user2@email.com',
            password = bcrypt.generate_password_hash('password123').decode('utf-8')
        )
    ]

    restaurants = [
        Restaurant(
            name = 'Macdonalds',
            address = '123 main st',
            is_vegan = False,
            price_range = '$'
        ),
        Restaurant(
            name = 'Burger King',
            address = '456 high st',
            is_vegan = False,
            price_range = '$$'
        ),
        Restaurant(
            name = 'Veggie Hut',
            address = '789 low st',
            is_vegan = True,
            price_range = '$'
        ),
        Restaurant(
            name = 'Laksa Palace',
            address = '1011 high st',
            is_vegan = True,
            price_range = '$$'
        )
    ]

    db.session.add_all(restaurants)
    db.session.add_all(users)
    db.session.commit()
    print('Table seeded')

@app.cli.command('drop')
def drop_db():
    db.drop_all()
    print("Tables dropped")




@app.route('/auth/register', methods=['POST'])
def auth_register():
    try:
        #Create a new user model instance from the user info
        user = User(
            username = request.json['username'],
            email = request.json['email'],
            password = bcrypt.generate_password_hash(request.json['password']).decode('utf-8')
        )
        #Add the new user to the database
        db.session.add(user)
        db.session.commit()
        #Return a response with the new user's info
        return UserSchema(exclude=['password']).dump(user), 201
    except IntegrityError:
        return {'error':'Email address already in use'}, 409

@app.route('/auth/login', methods= ['POST'])
def auth_login():
    #Find a user model instance from the user info
    stmt = db.select(User).filter_by(email=request.json['email'])
    user = db.session.scalar(stmt)
    #Check if the hashed password matches the user's password
    if user and bcrypt.check_password_hash(user.password, request.json['password']):
        #Return a response with the user's info
        token =create_access_token(identity=str(user.id),expires_delta=timedelta(days=1))
        return {'username':user.username, 'email':user.email, 'token':token, 'is_admin':user.is_admin}, 200
    else:
        return {'error':'Incorrect email or password'}, 401

 
@app.route('/restaurants/')
@jwt_required()
def all_restaurants():
    if not authorize():
        return {'error':'You must be an admin'}, 401
    stmt = db.select(Restaurant)
    restaurants = db.session.scalars(stmt).all()
    return RestaurantSchema(many=True).dump(restaurants)

@app.cli.command('all_restaurants_address')
def all_restaurants_address():
    stmt = db.select(Restaurant.name, Restaurant.address)
    restaurants = db.session.execute(stmt)
    print ('\n')
    for restaurant in restaurants:
        print(restaurant)

@app.cli.command('all_restaurants_vegan')
def all_restaurants_vegan():
    stmt = db.select(Restaurant.name).filter_by(is_vegan = True)
    restaurants = db.session.scalars(stmt)
    print ('\n')
    for restaurant in restaurants:
        print(restaurant)

@app.cli.command('all_restaurants_vegan_cheap')
def all_restaurants_vegan_cheap():
    stmt = db.select(Restaurant.name).order_by(Restaurant.name).where(db.or_(Restaurant.is_vegan == True, Restaurant.price_range == '$'))
    restaurants = db.session.scalars(stmt)
    print ('\n')
    for restaurant in restaurants:
        print(restaurant)


@app.cli.command('first_restaurant')
def first_restaurant():
    stmt =db.select(Restaurant).limit(1)
    restaurant = db.session.scalar(stmt)
    print('\n')
    print(restaurant.__dict__)


@app.cli.command('count_vegan')
def count_vegan():
    stmt = db.select(db.func.count()).select_from(Restaurant).filter_by(is_vegan=True)
    restaurants = db.session.scalar(stmt)
    print(restaurants)


@app.route('/')
def index():
    return 'hello world!'