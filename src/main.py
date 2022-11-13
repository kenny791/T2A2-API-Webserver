from flask import Flask
from marshmallow.exceptions import ValidationError
from init import db, ma, bcrypt, jwt
from controllers.restaurant_controller import restaurants_bp
from controllers.auth_controller import auth_bp
# from controllers.saved_controller import saved_bp
from controllers.profile_controller import profiles_bp
from controllers.cli_controller import db_commands
import os


# Instantiate Flask app
def create_app():
    app = Flask(__name__)

    #error handlers for different types of error codes
    @app.errorhandler(404)
    def not_found(err):
        return {'error': str(err)}, 404

    @app.errorhandler(401)
    def unauthorized(err):
        return {'error': str(err)}, 401

    @app.errorhandler(400)
    def bad_request(err):
        return {'error': f'Body cannot be empty'}, 400

    @app.errorhandler(ValidationError)
    def bad_request(err):
        return {'error': err.messages}, 400

    @app.errorhandler(KeyError)
    def key_error(err):
        return {'error': f'The field {err} is required.'}, 400

    
    # database configuration
    app.config['JSON_SORT_KEYS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

    # instances of the different libraries used for the app
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)


    # blueprints for different routes to be registered app instance
    app.register_blueprint(restaurants_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(db_commands)
    app.register_blueprint(profiles_bp)
   




    return app