# from flask import Blueprint
# from init import db, bcrypt
# from datetime import date
# from models.restaurant import Restaurant
# from models.user import User

# db_commands = Blueprint('db', __name__)

# # Define a custom CLI (terminal) command
# @db_commands.cli.command('create')
# def create_db():
#     db.create_all()
#     print("Tables created")

# @db_commands.cli.command('drop')
# def drop_db():
#     db.drop_all()
#     print("Tables dropped")

# @db_commands.cli.command('seed')
# def seed_db():
#     users = [
#         User(
#             username="admin",
#             email='admin@email.com',
#             password=bcrypt.generate_password_hash('admin').decode('utf-8'),
#             is_admin=True
#         ),
#         User(
#             username="user1",
#             email='user1@email.com',
#             password=bcrypt.generate_password_hash('user1').decode('utf-8')
#         )
#     ]

#     restaurants = [
#         Restaurant(
#             name = 'Start the project',
#             address = '123 main st',
#             is_vegan = True,
#             price_range = '$',
#         )
#     ]

#     db.session.add_all(restaurants)
#     db.session.add_all(users)
#     db.session.commit()
#     print('Tables seeded')