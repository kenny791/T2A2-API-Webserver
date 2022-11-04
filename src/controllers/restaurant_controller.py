from flask import Blueprint, request
from db import db
from models.restaurant import Restaurant, RestaurantSchema

restaurants_bp = Blueprint('restaurants', __name__, url_prefix='/restaurants')

@restaurants_bp.route('/')
def get_all_restaurants():
    stmt = db.select(Restaurant)
    restaurants = db.session.scalars(stmt)
    return RestaurantSchema(many=True).dump(restaurants)

@restaurants_bp.route('/vf/')
def get_is_vegan_restaurants():
    stmt = db.select(Restaurant).filter_by(is_vegan=True).order_by(Restaurant.price_range.desc())
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
def add_restaurant():
    restaurant = Restaurant(
        name = request.json['name'],
        address = request.json['address'],
        price_range = request.json['price_range'],
        is_vegan = request.json['is_vegan']
    )
    #Add the restaurant to the database
    db.session.add(restaurant)
    db.session.commit()
    #Returning a response with the new restaurant's info
    return RestaurantSchema().dump(restaurant), 201

@restaurants_bp.route('/<int:id>/', methods=['PUT','PATCH'])
def update_restaurant(id):
    stmt = db.select(Restaurant).filter_by(id=id)
    restaurant = db.session.scalar(stmt)
    if restaurant:
        restaurant.name = request.json.get('name') or restaurant.name
        restaurant.address = request.json.get('address') or restaurant.address
        restaurant.price_range = request.json.get('price_range') or restaurant.price_range
        restaurant.is_vegan = request.json.get('is_vegan') or restaurant.is_vegan
        db.session.commit()
        return RestaurantSchema().dump(restaurant)
    else:
        return {'error': f'Restaurant not found with id {id}'}, 404

@restaurants_bp.route('/<int:id>/', methods=['DELETE'])
def delete_restaurant(id):
    stmt = db.select(Restaurant).filter_by(id=id)
    restaurant = db.session.scalar(stmt)
    if restaurant:
        db.session.delete(restaurant)
        db.session.commit()
        return {'message': f'Restaurant \'{restaurant.name}\' with id \'{id}\' deleted successfully'},200
    else:
        return {'error': f'Restaurant not found with id {id}'}, 404