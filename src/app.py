from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://db_dev:password123@127.0.0.1:5432/food_finder'


db = SQLAlchemy(app)

#creates table
class Restaurant(db.Model):
    __tablename__ ='restaurants'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String())
    address = db.Column(db.String())
    is_vegan = db.Column(db.Boolean())
    price_range = db.Column(db.String())

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
            price_range = '$'
        ),
        Restaurant(
            name = 'Veggie Hut',
            address = '789 low st',
            is_vegan = True,
            price_range = '$$'
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




@app.cli.command('all_restaurants')
def all_restaurants():
    stmt = db.select(Restaurant)
    restaurants = db.session.scalars(stmt).all()
    print ('\n')
    for restaurant in restaurants:
        print(restaurant.__dict__)


@app.cli.command('first_restaurant')
def first_restaurant():
    #select * from cards limit 1;
    restaurant =Restaurant.query.first()
    print('\n')
    print(restaurant.__dict__)







@app.route('/')
def index():
    return 'hello world!'