from flask import Blueprint, request
from init import db
from models.restaurant import Restaurant, RestaurantSchema
from models.saved import Saved, SavedSchema
from models.review import Review, ReviewSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.auth_controller import authorize, authorize_user
from email import message
from datetime import date

saved_bp = Blueprint('saved', __name__, url_prefix='/saved')


# displays all saved restaurants for a user
@saved_bp.route('/')
@jwt_required()
def get_user_saved():
    user_id = get_jwt_identity()
    stmt = db.select(Saved).filter_by(user_id=user_id)
    saved = db.session.scalars(stmt)
    #return restaurant name and id
    return SavedSchema(many=True).dump(saved)

# delete saved by user_id
@saved_bp.route('/<int:saved_id>/', methods=['DELETE'])
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