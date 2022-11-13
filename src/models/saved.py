from init import db, ma
from marshmallow import fields, validates
from marshmallow.validate import Email, OneOf, And, Regexp, Length
from marshmallow.exceptions import ValidationError

# sqlalchemy model, each object shown reflects a column in the table
class Saved(db.Model):
    __tablename__ = 'saved' #table name used for db

    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(10), nullable=True, default='')

    # foreign keys, are used to link the tables together
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)


    # stores all fields from User table into user object
    user = db.relationship ("User", back_populates='saved') # create a field in the user schema that displays the user's saved restaurants
    restaurant = db.relationship ("Restaurant", back_populates='saved') #create a field in the restaurant schema that displays the restaurant's saved in a users saved list

# marshmallow schema, used to validate data before it is sent to the db, and to format the data before it is sent to the client
class SavedSchema(ma.Schema):
    tag =fields.String(load_default='', 
        validate=OneOf(['Fave', 'To Go',''], error='Tag must be either Fave or To Go'))
    restaurant = fields.Nested('RestaurantSchema', only=['name'])

    # the fields that are sent to the client
    class Meta:
        fields = ('id', 'restaurant','tag')
        ordered = True

