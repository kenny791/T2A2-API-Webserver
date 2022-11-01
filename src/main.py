from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# creating database object, this is the core of the ORM
db = SQLAlchemy()

def create_app():
    # using a list comprehension and multiple assignment 
    # to grab the environment variables we need

    # creating the flask app object - this is the core of our app!
    app = Flask(__name__)

    # configuring our app:
    app.config.from_object("config.app_config")


    @app.route('/')
    def index():
        return 'Hello World!'

    # creating an instance of the database object
    db.init_app(app)


    return app