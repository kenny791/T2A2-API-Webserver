from flask import Blueprint, request
from init import db
from models.restaurant import Restaurant, RestaurantSchema
from models.pin import Pin, PinSchema
from models.review import Review, ReviewSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.auth_controller import authorize, authorize_user
from email import message
from datetime import date

pins_bp = Blueprint('pins', __name__, url_prefix='/pins')



#display all pinned restaurants for a user
@pins_bp.route('/')
@jwt_required()
def get_user_pins():
    user_id = get_jwt_identity()
    stmt = db.select(Pin).filter_by(user_id=user_id)
    pins = db.session.scalars(stmt)
    #return restaurant name and id
    return PinSchema(many=True).dump(pins)

# delete pin by user_id
@pins_bp.route('/<int:pin_id>/', methods=['DELETE'])
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