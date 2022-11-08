from init import db, ma
from marshmallow import fields
from marshmallow.validate import Email, OneOf, And, Regexp, Length
from marshmallow.exceptions import ValidationError

class Pin(db.Model):
    __tablename__ = 'pins'

    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)


#     # stores all fields from User table into user object
    user = db.relationship ("User", back_populates='pins')
    restaurant = db.relationship ("Restaurant", back_populates='pins')

class PinSchema(ma.Schema):
    class Meta:
        fields = ('id', 'tag','restaurant_id', 'user_id')