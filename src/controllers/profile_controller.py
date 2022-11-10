from flask import Blueprint, request
from init import db
from models.restaurant import Restaurant, RestaurantSchema
from models.saved import Saved, SavedSchema
from models.review import Review, ReviewSchema
from models.user import User, UserSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.auth_controller import is_admin, original_user
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
    return UserSchema(exclude=['password', 'is_admin', 'saved', 'reviews_submitted']).dump(user)


#display all savedned restaurants for user
@profiles_bp.route('/saved/')
@jwt_required()
def get_user_saved():
    user_id = get_jwt_identity()
    stmt = db.select(Saved).filter_by(user_id=user_id)
    saved = db.session.scalars(stmt)
    # if there are saved then display them
    if saved:
        return SavedSchema(many=True).dump(saved)
    else:
        return {'error': 'No saved found'}, 404
    

# delete saved by user_id
@profiles_bp.route('saved/<int:saved_id>/', methods=['DELETE'])
@jwt_required()
def delete_saved(saved_id):
    if original_user():
        stmt = db.select(Saved).filter_by(id=saved_id)
        saved = db.session.scalar(stmt)
        if saved:
            db.session.delete(saved)
            db.session.commit()
            return {'message': f'Saved {saved_id} deleted'}, 200
        else:
            return {'error': f'Saved not found with id {saved_id}'}, 404
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
        if original_user() == review.user_id or is_admin():
            db.session.delete(review)
            db.session.commit()
            return {'message': f'Review with id \'{review_id}\' deleted successfully'},200
        else:
            return {'error': 'You can only delete your own reviews'}, 401
    else:
        return {'error': f'Review not found with id {review_id}'}, 404
