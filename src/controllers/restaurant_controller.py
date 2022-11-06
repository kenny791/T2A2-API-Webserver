from flask import Blueprint, request
from init import db
from models.restaurant import Restaurant, RestaurantSchema
from models.review import Review, ReviewSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.auth_controller import authorize
from email import message
from datetime import date

restaurants_bp = Blueprint('restaurants', __name__, url_prefix='/restaurants')

@restaurants_bp.route('/')
def get_all_restaurants():
    stmt = db.select(Restaurant)
    restaurants = db.session.scalars(stmt)
    return RestaurantSchema(many=True).dump(restaurants)


@restaurants_bp.route('/<int:id>/')
def get_one_restaurant(id):
    stmt = db.select(Restaurant).filter_by(id=id)
    restaurant = db.session.scalar(stmt)
    if restaurant:
        return RestaurantSchema().dump(restaurant)
    else:
        return {'error': f'Restaurant not found with id {id}'}, 404

@restaurants_bp.route('/', methods=['POST'])
@jwt_required()
def add_restaurant():
    data = RestaurantSchema().load(request.json)
    restaurant = Restaurant(
        name = data['name'],
        region = data['region'],
        price_range = data['price_range'],
        cuisine = data['cuisine'],
        user_id = get_jwt_identity()
    )
    #Add the restaurant to the database
    db.session.add(restaurant)
    db.session.commit()
    #Returning a response with the new restaurant's info
    return RestaurantSchema(exclude = ['reviews', 'added_by']).dump(restaurant), 201

@restaurants_bp.route('/<int:id>/', methods=['PUT','PATCH'])
@jwt_required()
def update_restaurant(id):
    stmt = db.select(Restaurant).filter_by(id=id)
    restaurant = db.session.scalar(stmt)


    if restaurant:
        data = RestaurantSchema().load(request.json)
        restaurant.name = data['name'] or restaurant.name
        restaurant.region = data['region'] or restaurant.region
        restaurant.price_range = data['price_range'] or restaurant.price_range
        restaurant.cuisine = data['cuisine'] or restaurant.cuisine
        
        db.session.commit()
        return RestaurantSchema(exclude=['reviews']).dump(restaurant), 200
    else:
        return {'error': f'Restaurant not found with id {id}'}, 404

@restaurants_bp.route('/<int:id>/', methods=['DELETE'])
@jwt_required()
def delete_restaurant(id):
    if not authorize():
        return {'error': 'You must be an admin'}, 401
    stmt = db.select(Restaurant).filter_by(id=id)
    restaurant = db.session.scalar(stmt)
    if restaurant:
        db.session.delete(restaurant)
        db.session.commit()
        return {'message': f'Restaurant \'{restaurant.name}\' with id \'{id}\' deleted successfully'},200
    else:
        return {'error': f'Restaurant not found with id {id}'}, 404

@restaurants_bp.route('/<int:restaurant_id>/review/', methods=['POST'])
@jwt_required()
def create_review(restaurant_id):
    stmt = db.select(Restaurant).filter_by(id=restaurant_id)
    restaurant = db.session.scalar(stmt)
    if restaurant:
        review = Review(
            user_id = get_jwt_identity(),
            message = request.json['message'],
            rating = request.json['rating'],
            restaurant = restaurant,
            date = date.today(),
        )
        db.session.add(review)
        db.session.commit()
        return ReviewSchema().dump(review), 201
    else:
        return {'error': f'Restaurant not found with id {id}'}, 404
