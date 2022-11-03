from flask import Blueprint
from db import db
from models.restaurant import Restaurant, RestaurantSchema

restaurants_bp = Blueprint('restaurants', __name__, url_prefix='/restaurants')

@restaurants_bp.route('/')
# @jwt_required()
def all_restaurants():
    return 'all restaurants'
    stmt = db.select(Restaurant).order_by(Restaurant.name)
    restaurants = db.session.scalars(stmt)
    return RestaurantSchema(many=True).dump(restaurants)


