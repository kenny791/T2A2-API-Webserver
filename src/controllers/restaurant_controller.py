from flask import Blueprint, request
from init import db
from models.restaurant import Restaurant, RestaurantSchema
from models.saved import Saved, SavedSchema
from models.review import Review, ReviewSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.auth_controller import is_admin, original_user
from email import message
from datetime import date

restaurants_bp = Blueprint('restaurants', __name__, url_prefix='/restaurants')

# route returns all restaurants in the database sorted by name
@restaurants_bp.route('/')
def get_all_restaurants():
    stmt = db.select(Restaurant).order_by(Restaurant.name)
    restaurants = db.session.scalars(stmt)
    return RestaurantSchema(many=True, exclude = ['reviews','tagged_to_go','tagged_fave']).dump(restaurants)


# route displays a single restaurant by id, with more details such as reviews and tags
@restaurants_bp.route('/<int:id>/')
@jwt_required()
def get_one_restaurant(id):
    stmt = db.select(Restaurant).filter_by(id=id)
    restaurant = db.session.scalar(stmt)
    if restaurant:
        return RestaurantSchema().dump(restaurant)
    else:
        return {'error': f'Restaurant not found with id {id}'}, 404


# route displays restaurants of a specific cuisine
@restaurants_bp.route('/cuisine/<cuisine>/')
def get_restaurants_by_cuisine(cuisine):
    #check cuisine is available
    stmt = db.select(Restaurant).filter_by(cuisine=cuisine.title()).order_by(Restaurant.name)
    restaurants = db.session.scalars(stmt)
    if restaurants:
        return RestaurantSchema(many=True, exclude = ['reviews','tagged_to_go','tagged_fave']).dump(restaurants)
    else:
        return {'error': f'Restaurant not found with cuisine {cuisine}'}, 404


# route displays restaurants of a specific location
@restaurants_bp.route('/location/<location>/')
def get_restaurants_by_location(location):
    stmt = db.select(Restaurant).filter_by(location=location.title()).order_by(Restaurant.name)
    restaurants = db.session.scalars(stmt)
    if restaurants:
        return RestaurantSchema(many=True, exclude = ['reviews','tagged_to_go','tagged_fave']).dump(restaurants)
    else:
        return {'error': f'Restaurant not found with location {location}'}, 404


# route displays all restaurants sorted by price range (low to high)
@restaurants_bp.route('/price/<sort>/')
def get_restaurants_by_price(sort):
    if sort.lower() == 'low':
        return get_restaurants_by_price_range_low()
    elif sort.lower() == 'high':
        return get_restaurants_by_price_range_high()
    else:
        return {'error': f'{sort} Price sort not found'}, 404

def get_restaurants_by_price_range_low():
    stmt = db.select(Restaurant).order_by(Restaurant.price_range).order_by(Restaurant.name)
    restaurants = db.session.scalars(stmt)
    return RestaurantSchema(many=True, exclude = ['reviews','tagged_to_go','tagged_fave']).dump(restaurants)

def get_restaurants_by_price_range_high():
    stmt = db.select(Restaurant).order_by(Restaurant.price_range.desc())
    restaurants = db.session.scalars(stmt)
    return RestaurantSchema(many=True, exclude = ['reviews','tagged_to_go','tagged_fave']).dump(restaurants)


# route adds a new restaurant to db
@restaurants_bp.route('/submit/', methods=['POST'])
@jwt_required()
def add_restaurant():
    data = RestaurantSchema().load(request.json)
    #check if existing
    stmt = db.select(Restaurant).filter_by(name=data['name'])
    restaurant = db.session.scalar(stmt)
    if restaurant:
        return {'error': f'Restaurant \'{data["name"]}\' already exists'}, 400
    else:
        restaurant = Restaurant(
            name = data['name'],
            location = data['location'],
            price_range = data['price_range'],
            cuisine = data['cuisine'],
        )
    #Add the restaurant to the database
    db.session.add(restaurant)
    db.session.commit()
    #Returning a response with the new restaurant's info
    return RestaurantSchema(exclude = ['reviews','tagged_to_go','tagged_fave','avg_rating', 'saved_for_later']).dump(restaurant), 201


# route updates the details of a restaurant by id
@restaurants_bp.route('/<int:id>/', methods=['PUT','PATCH'])
@jwt_required()
def update_restaurant(id):
    stmt = db.select(Restaurant).filter_by(id=id)
    restaurant = db.session.scalar(stmt)
    if restaurant:
        data = RestaurantSchema().load(request.json)
        restaurant.name = data['name'] or restaurant.name
        restaurant.location = data['location'] or restaurant.location
        restaurant.price_range = data['price_range'] or restaurant.price_range
        restaurant.cuisine = data['cuisine'] or restaurant.cuisine
        
        db.session.commit()
        return RestaurantSchema(exclude = ['reviews','tagged_to_go','tagged_fave','avg_rating', 'saved_for_later']).dump(restaurant), 200
    else:
        return {'error': f'Restaurant not found with id \'{id}\''}, 404


# route deletes a restaurant by id
@restaurants_bp.route('/<int:id>/', methods=['DELETE'])
@jwt_required()
def delete_restaurant(id):
    if not is_admin():
        return {'error': 'You must be an admin'}, 401
    stmt = db.select(Restaurant).filter_by(id=id)
    restaurant = db.session.scalar(stmt)
    if restaurant:
        db.session.delete(restaurant)
        db.session.commit()
        return {'message': f'Restaurant \'{restaurant.name}\' with id \'{id}\' deleted successfully'},200
    else:
        return {'error': f'Restaurant not found with id {id}'}, 404


# route posts a review for a specific restaurant
@restaurants_bp.route('/<int:restaurant_id>/review/', methods=['POST'])
@jwt_required()
def create_review(restaurant_id):
    stmt = db.select(Restaurant).filter_by(id=restaurant_id)
    restaurant = db.session.scalar(stmt)
    if restaurant:
        # if no existing review by user, create new review
        stmt = db.select(Review).filter_by(user_id=get_jwt_identity(), restaurant_id=restaurant_id)
        review = db.session.scalar(stmt)
        if not review:
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
            return {'error': f'You have already reviewed this restaurant'}, 400
    else:
        return {'error': f'Restaurant not found with id {id}'}, 404


# route updates a review for a specific restaurant
@restaurants_bp.route('/<int:restaurant_id>/review/', methods=['PUT','PATCH'])
@jwt_required()
def update_review(restaurant_id,):
    stmt = db.select(Restaurant).filter_by(id=restaurant_id)
    restaurant = db.session.scalar(stmt)
    if restaurant:
        # if existing review by user, update review
        stmt = db.select(Review).filter_by(user_id=get_jwt_identity(), restaurant_id=restaurant_id)
        review = db.session.scalar(stmt)
        if review:
            data = ReviewSchema().load(request.json)
            review.rating = data['rating'] or review.rating
            review.message = data['message'] or review.message
            review.date = date.today()
            db.session.commit()
            return ReviewSchema().dump(review), 200
        else:
            return {'error': f'You have not reviewed this restaurant'}, 400
    else:
        return {'error': f'Restaurant not found with id {id}'}, 404


# route deletes a review of a restaurant by id
@restaurants_bp.route('/<int:restaurant_id>/review/<int:review_id>/', methods=['DELETE'])
@jwt_required()
def delete_review(restaurant_id, review_id):
    stmt = db.select(Review).filter_by(id=review_id)
    review = db.session.scalar(stmt)
    user = get_jwt_identity()
    if review:
        if original_user() == review.user_id or is_admin():
            db.session.delete(review)
            db.session.commit()
            return {'message': f'Review with id \'{review_id}\' deleted successfully'},200
        else:
            return {'error': 'You can only delete your own reviews'}, 401
    else:
        return {'error': f'Review not found with id {review_id}'}, 404



# route adds a restaurant to a users saved list
@restaurants_bp.route('/<int:restaurant_id>/save/', methods=['POST'])
@jwt_required()
def add_restaurant_to_saved(restaurant_id):
    stmt = db.select(Restaurant).filter_by(id=restaurant_id)
    restaurant = db.session.scalar(stmt)
    stmt = db.select(Saved).filter_by(user_id=get_jwt_identity(), restaurant_id=restaurant_id)
    saved = db.session.scalar(stmt)
    data = SavedSchema().load(request.json)
    
    # return {'message': f'saved with tag {saved} found' },200
    if saved == None: #if saved doesn't exist, add a new entry to the database with any received tag data
        saved = Saved(
            tag = data['tag'],
            user_id = get_jwt_identity(),
            restaurant_id = restaurant_id
        )
        db.session.add(saved)
        db.session.commit()
        return {'message': f'Restaurant \'{restaurant.name}\' added to your saved restaurants successfully'},200
    else:
        if saved.tag == data['tag']:
            return {'message': f'Restaurant \'{restaurant.name}\' already in saved list with tag \'{saved.tag}\''},200
        else:
            return {'message': f'Restaurant \'{restaurant.name}\' already in saved list'},200


# route updates the tag to a saved restaurant
@restaurants_bp.route('/<int:restaurant_id>/save/', methods=['PUT','PATCH'])
@jwt_required()
def update_saved_tag(restaurant_id):
    stmt = db.select(Saved).filter_by(user_id=get_jwt_identity(), restaurant_id=restaurant_id)
    saved = db.session.scalar(stmt)
    data = SavedSchema().load(request.json)
    if saved:
        saved.tag = data['tag']
        db.session.commit()
        return {'message': f'Tag for saved restaurant with id \'{restaurant_id}\' updated successfully'},200
    else:
        return {'error': f'Saved restaurant not found with id {restaurant_id}'}, 404


# route deletes a restaurant from a users saved list
@restaurants_bp.route('<int:restaurant_id>/save/', methods=['DELETE'])
@jwt_required()
def delete_saved_restaurant(restaurant_id):
    stmt = db.select(Saved).filter_by(user_id=get_jwt_identity(), restaurant_id=restaurant_id)
    saved = db.session.scalar(stmt)
    if saved:
        db.session.delete(saved)
        db.session.commit()
        return {'message': f'Restaurant with id \'{restaurant_id}\' deleted from your saved list successfully'},200
    else:
        return {'error': f'Restaurant with id \'{restaurant_id}\' not found in saved list'}, 404




