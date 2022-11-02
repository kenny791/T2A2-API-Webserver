from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app = Flask(__name__)
app.config ['JSON_SORT_KEYS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://db_dev:password123@127.0.0.1:5432/food_finder'


db = SQLAlchemy(app)
ma = Marshmallow(app)

#creates table
class Restaurant(db.Model):
    __tablename__ ='restaurants'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String())
    address = db.Column(db.String())
    is_vegan = db.Column(db.Boolean())
    price_range = db.Column(db.String())


class RestaurantSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'address', 'is_vegan', 'price_range')
        ordered = True



#Defining a custom CLI (terminal) command
@app.cli.command('create')
def create_db():
    db.create_all()
    print("Tables created")



#adds entity
@app.cli.command('seed')
def seed_db():

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
    db.session.commit()
    print('Table seeded')

@app.cli.command('drop')
def drop_db():
    db.drop_all()
    print("Tables dropped")



@app.route('/restaurants/')
def all_restaurants():
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
def all_restaurants_vegan():
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