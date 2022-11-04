from flask import Blueprint, request
from db import db
from models.restaurant import Restaurant, RestaurantSchema

restaurants_bp = Blueprint('restaurants', __name__, url_prefix='/restaurants')

@restaurants_bp.route('/')
def all_restaurants():
    stmt = db.select(Restaurant)
    restaurants = db.session.scalars(stmt)
    return RestaurantSchema(many=True).dump(restaurants)

@restaurants_bp.route('/<int:id>/')
def one_restaurant(id):
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
