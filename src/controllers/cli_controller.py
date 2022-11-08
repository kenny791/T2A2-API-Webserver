from flask import Blueprint
from init import db, bcrypt
from datetime import date
from models.restaurant import Restaurant
from models.user import User
from models.review import Review
from models.pin import Pin

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
            password=bcrypt.generate_password_hash('passwordadmin').decode('utf-8'),
            is_admin=True
        ),
        User(
            username="user1",
            email='user1@email.com',
            password=bcrypt.generate_password_hash('password1').decode('utf-8')
        ),
        User(
            username="user2",
            email='user2@email.com',
            password=bcrypt.generate_password_hash('password2').decode('utf-8')
        ),
        User(
            username="user3",
            email='user3@email.com',
            password=bcrypt.generate_password_hash('password3').decode('utf-8')
        ),
        User(
            username="user4",
            email='user4@email.com',
            password=bcrypt.generate_password_hash('password4').decode('utf-8')
        ),
        User(
            username="user5",
            email="user5@email.com",
            password=bcrypt.generate_password_hash('password5').decode('utf-8')
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

# review seed data
    reviews = [
        Review(
            restaurant = restaurants[0],
            message = 'This place is great!',
            rating = 5,
            date = '2022-10-01',
            user = users[1]
        ),
        Review(
            restaurant = restaurants[0],
            message = 'Fantastic food and service!',
            rating = 4,
            date = date.today(),
            user = users[2]
        ),
        Review(
            restaurant = restaurants[0],
            message = 'Good but not great.',
            rating = 1,
            date = '2022-11-01',
            user = users[3]
        ),
        Review(
            restaurant = restaurants[1],
            message = 'This place is great!',
            rating = 5,
            date = '2022-10-01',
            user = users[1]
        ),
        Review(
            restaurant = restaurants[1],
            message = 'Fantastic food and service!',
            rating = 4,
            date = date.today(),
            user = users[2]
        ),
        Review(
            restaurant = restaurants[1],
            message = 'Good but not great.',
            rating = 1,
            date = '2022-10-01',
            user = users[3]
        ),
        Review(
            restaurant = restaurants[2],
            message = 'This place is great!',
            rating = 5,
            date = '2022-10-01',
            user = users[1]
        ),
        Review(
            restaurant = restaurants[2],
            message = 'Fantastic food and service!',
            rating = 4,
            date = date.today(),
            user = users[2]
        ),
        Review(
            restaurant = restaurants[2],
            message = 'Good but not great.',
            rating = 1,
            date = '2022-10-01',
            user = users[3]
        ),
        Review(
            restaurant = restaurants[3],
            message = 'This place is great!',
            rating = 5,
            date = '2022-10-01',
            user = users[1]
        ),
        Review(
            restaurant = restaurants[3],
            message = 'Fantastic food and service!',
            rating = 4,
            date = date.today(),
            user = users[2]
        ),
        Review(
            restaurant = restaurants[3],
            message = 'Good but not great.',
            rating = 1,
            date = '2022-10-01',
            user = users[3]
        ),
        Review(
            restaurant = restaurants[4],
            message = 'This place is great!',
            rating = 5,
            date = '2022-10-01',
            user = users[1]
        ),
        Review(
            restaurant = restaurants[4],
            message = 'Fantastic food and service!',
            rating = 4,
            date = '2022-10-01',
            user = users[2]
        ),
        Review(
            restaurant = restaurants[4],
            message = 'Good but not great.',
            rating = 1,
            date = date.today(),
            user = users[3]
        ),
        Review(
            restaurant = restaurants[5],
            message = 'This place is great!',
            rating = 5,
            date = '2022-10-01',
            user = users[1]
        ),
        Review(
            restaurant = restaurants[5],
            message = 'Fantastic food and service!',
            rating = 4,
            date = date.today(),
            user = users[2]
        ),
        Review(
            restaurant = restaurants[5],
            message = 'Good but not great.',
            rating = 1,
            date = '2022-10-01',
            user = users[3]
        ),
        Review(
            restaurant = restaurants[6],
            message = 'This place is great!',
            rating = 5,
            date = '2022-10-01',
            user = users[1]
        ),
        Review(
            restaurant = restaurants[6],
            message = 'Fantastic food and service!',
            rating = 4,
            date = date.today(),
            user = users[2]
        ),
        Review(
            restaurant = restaurants[6],
            message = 'Good but not great.',
            rating = 1,
            date = '2022-10-01',
            user = users[3]
        ),
        Review(
            restaurant = restaurants[7],
            message = 'This place is great!',
            rating = 5,
            date = '2022-10-01',
            user = users[1]
        ),
        Review(
            restaurant = restaurants[7],
            message = 'Fantastic food and service!',
            rating = 4,
            date = date.today(),
            user = users[2]
        ),
        Review(
            restaurant = restaurants[7],
            message = 'Good but not great.',
            rating = 1,
            date = '2022-10-01',
            user = users[3]
        ),
        Review(
            restaurant = restaurants[8],
            message = 'This place is great!',
            rating = 5,
            date = '2022-10-01',
            user = users[1]
        ),
        Review(
            restaurant = restaurants[8],
            message = 'Fantastic food and service!',
            rating = 4,
            date = date.today(),
            user = users[2]
        ),
        Review(
            restaurant = restaurants[8],
            message = 'Good but not great.',
            rating = 1,
            date = '2022-10-01',
            user = users[3]
        )
    ]


    db.session.add_all(reviews)
    db.session.commit()


    pins = [
        Pin(
            tag = 'fave',
            restaurant = restaurants[0],
            user = users[5]
        ),
        Pin(
            tag = 'visit',
            restaurant = restaurants[1],
            user = users[5]
        ),
        Pin(
            restaurant = restaurants[2],
            user = users[5]
        )
    ]

    db.session.add_all(pins)
    db.session.commit()
    print('Tables seeded')