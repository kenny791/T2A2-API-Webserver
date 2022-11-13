from init import db, ma
from marshmallow import fields
from marshmallow.validate import Email, OneOf, And, Regexp, Length
from marshmallow.exceptions import ValidationError

# list of valid data that can inputted into the rating field
VALID_RATING = [0,1,2,3,4,5]

# sqlalchemy model, each object shown reflects a column in the table
class Review(db.Model):
    __tablename__ = 'reviews' #table name used for db

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255))
    rating = db.Column(db.Integer,)
    date = db.Column(db.Date)

    # foreign keys, are used to link the tables together
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False) 

    # stores all fields from User table into user object
    user = db.relationship ("User", back_populates='reviews_submitted') # creates a field the user schema that displays the user's reviews
    restaurant = db.relationship ("Restaurant", back_populates='reviews')   # creates a field the restaurant schema that displays the restaurant's reviews
    
   
# marshmallow schema, used to validate data before it is sent to the db, and to format the data before it is sent to the client
class ReviewSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['id','username'])
    restaurant = fields.Nested('RestaurantSchema', only=['name'])
    message = fields.String(validate=And( 
        Length(min=1, error='Message must be at least 1 character long'),
        Length(max=255, error='Message must be less than 255 characters long')
        ))
    rating = fields.Integer(validate = OneOf(VALID_RATING), error = 'Rating must be between 1 and 5')

    # the fields that are sent to the client
    class Meta:
        fields = ('id', 'restaurant', 'date','rating', 'message','user')
        ordered = True





