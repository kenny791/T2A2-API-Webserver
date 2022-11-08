from init import db, ma
from marshmallow import fields, validates
from marshmallow.validate import Email, OneOf, And, Regexp, Length
from marshmallow.exceptions import ValidationError


class Pin(db.Model):
    __tablename__ = 'pins'

    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(50), nullable=True, default='')

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)


#     # stores all fields from User table into user object
    user = db.relationship ("User", back_populates='pins')
    restaurant = db.relationship ("Restaurant", back_populates='pins')

class PinSchema(ma.Schema):
    tag =fields.String(load_default='', 
        validate=OneOf(['Fave', 'To Go',''], error='Tag must be either Fave or To Go'))
    restaurant = fields.Nested('RestaurantSchema', only=['name'])

    class Meta:
        fields = ('id', 'restaurant','tag','user_id')
        ordered = True