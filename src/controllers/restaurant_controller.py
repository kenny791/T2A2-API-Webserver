from flask import Blueprint
from db import db
from models.restaurant import Restaurant, RestaurantSchema

restaurants_bp = Blueprint('restaurants', __name__, url_prefix='/restaurants')

@restaurants_bp.route('/')
def all_restaurants():
    stmt = db.select(Restaurant)
    restaurants = db.session.scalars(stmt)
    return RestaurantSchema(many=True).dump(restaurants)

@restaurants_bp.route('/<int:id>/')
def one_restaurants(id):
    stmt = db.select(Restaurant).filter_by(id=id)
    restaurant = db.session.scalar(stmt)
    return RestaurantSchema().dump(restaurant)
