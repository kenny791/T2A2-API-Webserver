from flask import Blueprint, request
from init import db
from models.restaurant import Restaurant, RestaurantSchema
from models.pin import Pin, PinSchema
from models.review import Review, ReviewSchema
from models.user import User, UserSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.auth_controller import authorize, authorize_user
from email import message
from datetime import date

profiles_bp = Blueprint('profile', __name__, url_prefix='/profile')



# display user profile
@profiles_bp.route('/')
@jwt_required()
def get_user_profile():
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    return UserSchema(exclude=['password', 'is_admin', 'pins', 'reviews_submitted']).dump(user)


#display all pinned restaurants for user
@profiles_bp.route('/pins/')
@jwt_required()
def get_user_pins():
    user_id = get_jwt_identity()
    stmt = db.select(Pin).filter_by(user_id=user_id)
    pins = db.session.scalars(stmt)
    # if there are pins then display them
    if pins:
        return PinSchema(many=True).dump(pins)
    else:
        return {'error': 'No pins found'}, 404
    

# delete pin by user_id
@profiles_bp.route('pins/<int:pin_id>/', methods=['DELETE'])
@jwt_required()
def delete_pin(pin_id):
    if authorize_user():
        stmt = db.select(Pin).filter_by(id=pin_id)
        pin = db.session.scalar(stmt)
        if pin:
            db.session.delete(pin)
            db.session.commit()
            return {'message': f'Pin {pin_id} deleted'}, 200
        else:
            return {'error': f'Pin not found with id {pin_id}'}, 404
    else:
        return {'error': 'Unauthorized'}, 401


#display all reviews for user
@profiles_bp.route('/reviews/')
@jwt_required()
def get_user_reviews():
    user_id = get_jwt_identity()
    stmt = db.select(Review).filter_by(user_id=user_id)
    reviews = db.session.scalars(stmt)
    return ReviewSchema(many=True, exclude=['user']).dump(reviews)





#delete a review
@profiles_bp.route('/reviews/<int:review_id>/', methods=['DELETE'])
@jwt_required()
def delete_review(review_id):
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
