from unicodedata import name, jsonify
from flask import Flask
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
    print("tables created")



#adds entity
@app.cli.command('seed')
def seed_db():
    restaurant = Restaurant(
        name = 'Macdonalds',
        address = '123 main st',
        is_vegan = False,
        price_range = '$',
    )

    db.session.add(restaurant)
    db.session.commit()
    print('Table seeded')

@app.cli.command('drop')
def drop():
    db.drop_all()
    print("Tables dropped")




@app.route('/')
def index():
    return 'hello world!'