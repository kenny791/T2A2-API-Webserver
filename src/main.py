from flask import Flask
from init import db, ma, bcrypt, jwt
from controllers.restaurant_controller import restaurants_bp
from controllers.auth_controller import auth_bp
from controllers.saved_controller import saved_bp
from controllers.profile_controller import profiles_bp
from controllers.cli_controller import db_commands
import os
from marshmallow.exceptions import ValidationError


def create_app():
    app = Flask(__name__)

    #catches all 404 raised within app
    @app.errorhandler(404)
    def not_found(err):
        return {'error': str(err)}, 404

    @app.errorhandler(401)
    def unauthorized(err):
        return {'error': str(err)}, 401

    @app.errorhandler(ValidationError)
    def bad_request(err):
        return {'error': err.messages}, 400

    app.config['JSON_SORT_KEYS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')


    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)



    app.register_blueprint(restaurants_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(db_commands)
    app.register_blueprint(saved_bp)
    app.register_blueprint(profiles_bp)
   
    return app