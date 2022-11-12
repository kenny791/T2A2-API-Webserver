from init import db, ma
from marshmallow import fields, validates
from marshmallow.validate import Email, OneOf, And, Regexp, Length
from marshmallow.exceptions import ValidationError


class Saved(db.Model):
    __tablename__ = 'saved' #table name used for db

    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(10), nullable=True, default='')

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)


    # stores all fields from User table into user object
    user = db.relationship ("User", back_populates='saved')
    restaurant = db.relationship ("Restaurant", back_populates='saved')

class SavedSchema(ma.Schema):
    tag =fields.String(load_default='', 
        validate=OneOf(['Fave', 'To Go',''], error='Tag must be either Fave or To Go'))
    restaurant = fields.Nested('RestaurantSchema', only=['name'])

    class Meta:
        fields = ('id', 'restaurant','tag')
        ordered = True

