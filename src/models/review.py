from init import db, ma
from marshmallow import fields
from marshmallow.validate import Email, OneOf, And, Regexp, Length
from marshmallow.exceptions import ValidationError

class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String)
    rating = db.Column(db.Integer)
    date = db.Column(db.Date) #Date created

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)

    # stores all fields from User table into user object
    user = db.relationship ("User", back_populates='reviews_submitted')
    restaurant = db.relationship ("Restaurant", back_populates='reviews')


class ReviewSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['username'])
    restaurant = fields.Nested('RestaurantSchema', only=['name'])
    message = fields.String(validate = Length(max=255, error='Message must be less than 255 characters long'))
    rating = fields.Integer(validate = OneOf([1,2,3,4,5]), error = 'Rating must be between 1 and 5')


    class Meta:
        fields = ('id', 'restaurant', 'date','rating', 'message','user')
        ordered = True