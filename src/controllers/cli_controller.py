from flask import Blueprint
from init import db, bcrypt
from datetime import date
from models.restaurant import Restaurant
from models.user import User
from models.review import Review

db_commands = Blueprint('db', __name__)

# Define a custom CLI (terminal) command

@db_commands.cli.command('drop')
def drop_db():
    db.drop_all()
    print("Tables dropped")

@db_commands.cli.command('create')
def create_db():
    db.create_all()
    print("Tables created")



@db_commands.cli.command('seed')
def seed_db():
    users = [
        User(
            username="admin",
            email='admin@email.com',
            password=bcrypt.generate_password_hash('admin').decode('utf-8'),
            is_admin=True
        ),
        User(
            username="user1",
            email='user1@email.com',
            password=bcrypt.generate_password_hash('user1').decode('utf-8')
        ),
        User(
            username="user2",
            email='user2@email.com',
            password=bcrypt.generate_password_hash('user2').decode('utf-8')
        ),
        User(
            username="user3",
            email='user3@email.com',
            password=bcrypt.generate_password_hash('user3').decode('utf-8')
        )
    ]

    db.session.add_all(users)
    db.session.commit()


    restaurants = [
        Restaurant(
            name = 'Mesa Verde',
            region = 'North',
            price_range = '$',
            cuisine = 'Mexican',
            user_id = users[1].id
        ),
        Restaurant(
            name = 'Minamishima',
            region = 'East',
            price_range = '$$',
            cuisine = 'Japanese',
            user_id = users[1].id
        ),
        Restaurant(
            name = 'Florentino',
            region = 'West',
            price_range = '$$$',
            cuisine = 'Italian',
            user_id = users[1].id
        ),
        Restaurant(
            name = 'Bodega Underground',
            region = 'North',
            price_range = '$$',
            cuisine = 'Mexican',
            user_id = users[2].id
        ),
        Restaurant(
            name = 'Nobu',
            region = 'South',
            price_range = '$$$',
            cuisine = 'Japanese',
            user_id = users[2].id
        ),
        Restaurant(
            name = 'Scopri',
            region = 'North',
            price_range = '$',
            cuisine = 'Italian',
            user_id = users[2].id
        ),
        Restaurant(
            name = 'Village Cantina',
            region = 'East',
            price_range = '$$$',
            cuisine = 'Mexican',
            user_id = users[3].id
        ),
        Restaurant(
            name = 'Supernormal',
            region = 'West',
            price_range = '$',
            cuisine = 'Japanese',
            user_id = users[3].id  
        ),
        Restaurant(
            name = 'Agostino',
            region = 'North',
            price_range = '$$',
            cuisine = 'Italian',
            user_id = users[3].id
        )
    ]

    db.session.add_all(restaurants)
    db.session.commit()

    reviews = [
        Review(
            message = 'This place is great!',
            rating = 5,
            date = date.today(),
            user = users[0],
            restaurant = restaurants[0]
        ),
        Review(
            message = 'This place is terrible!',
            rating = 1,
            date = date.today(),
            user = users[1],
            restaurant = restaurants[0]
        ),
        Review(
            message = 'This place is okay!',
            rating = 3,
            date = date.today(),
            user = users[2],
            restaurant = restaurants[0]
        ),
    ]


    db.session.add_all(reviews)
    db.session.commit()

    print('Tables seeded')