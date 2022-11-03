from flask import Flask
from db import db, ma
from controllers.restaurant_controller import restaurants_bp
# # from controllers.auth_controller import auth_bp
# # from controllers.cli_controller import db_commands
# from flask_bcrypt import Bcrypt
import os


def create_app():
    app = Flask(__name__)

    app.config['JSON_SORT_KEYS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')



    db.init_app(app)
    ma.init_app(app)



    app.register_blueprint(restaurants_bp)
#     # app.register_blueprint(auth_bp)
#     # app.register_blueprint(db_commands)
   


    return app

