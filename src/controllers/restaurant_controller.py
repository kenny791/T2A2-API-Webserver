from flask import Blueprint, request
from init import db
from models.restaurant import Restaurant, RestaurantSchema
from models.pin import Pin, PinSchema
from models.review import Review, ReviewSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.auth_controller import authorize, authorize_user
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
    return RestaurantSchema(exclude = ['reviews']).dump(restaurant), 201

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

#get all restaurants by cuisine

@restaurants_bp.route('/cuisine/<cuisine>/')
def get_restaurants_by_cuisine(cuisine):
    #check cuisine is available
    stmt = db.select(Restaurant).filter_by(cuisine=cuisine.title())
    restaurants = db.session.scalars(stmt)
    if restaurants:
        return RestaurantSchema(many=True).dump(restaurants)
    else:
        return {'error': f'Restaurant not found with cuisine {cuisine}'}, 404





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
        data = ReviewSchema().load(request.json)
        review = Review(
            user_id = get_jwt_identity(),
            restaurant_id = restaurant_id,
            rating = data['rating'],
            message = data['message'],
            date = date.today()
        )

        db.session.add(review)
        db.session.commit()
        return ReviewSchema().dump(review), 201
    else:
        return {'error': f'Restaurant not found with id {id}'}, 404


@restaurants_bp.route('/<int:restaurant_id>/review/<int:review_id>/', methods=['PUT','PATCH'])
@jwt_required()
def update_review(restaurant_id, review_id):
    stmt = db.select(Review).filter_by(id=review_id)
    review = db.session.scalar(stmt)
    data = ReviewSchema().load(request.json)
    user = get_jwt_identity()
    if review:
        if authorize_user() == review.user_id:
            review.rating = data['rating'] or review.rating
            review.message = data['message'] or review.message
            review.date = date.today()
            db.session.commit()
            return ReviewSchema().dump(review), 200
        else:
            return {'error': 'You can only update your own reviews'}, 401
    else:
        return {'error': f'Review not found with id {review_id}'}, 404


#delete a review
@restaurants_bp.route('/<int:restaurant_id>/review/<int:review_id>/', methods=['DELETE'])
@jwt_required()
def delete_review(restaurant_id, review_id):
    stmt = db.select(Review).filter_by(id=review_id)
    review = db.session.scalar(stmt)
    user = get_jwt_identity()
    if review:
        if authorize_user() == review.user_id or authorize():
            db.session.delete(review)
            db.session.commit()
            return {'message': f'Review with id \'{review_id}\' deleted successfully'},200
        else:
            return {'error': 'You can only delete your own reviews'}, 401
    else:
        return {'error': f'Review not found with id {review_id}'}, 404



# add restaurant to pins
@restaurants_bp.route('/<int:restaurant_id>/pin/', methods=['PATCH','PUT','POST'])
@jwt_required()
def add_restaurant_to_pins(restaurant_id):
    stmt = db.select(Restaurant).filter_by(id=restaurant_id)
    restaurant = db.session.scalar(stmt)
    stmt = db.select(Pin).filter_by(user_id=get_jwt_identity(), restaurant_id=restaurant_id)
    pin = db.session.scalar(stmt)
    data = PinSchema().load(request.json)
    # return {'message': f'pin with tag {pin} found' },200
    if pin == None: 
        pin = Pin(
            tag = data['tag'],
            user_id = get_jwt_identity(),
            restaurant_id = restaurant_id
        )
    else:
        pin.tag = data['tag'] or pin.tag
    db.session.add(pin)
    db.session.commit()
    return {'message': f'Restaurant \'{restaurant.name}\' with id \'{restaurant_id}\' added to pins successfully'},200

