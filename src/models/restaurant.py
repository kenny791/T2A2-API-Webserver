from init import db, ma
from marshmallow import fields, validates
from marshmallow.validate import Length, OneOf, And, Regexp
from marshmallow.exceptions import ValidationError


VALID_PRICE_RANGE = ['$', '$$', '$$$', '$$$$']
VALID_REGION = ['North', 'South', 'East', 'West']

class Restaurant(db.Model):
    __tablename__ = 'restaurants' #table name used for db
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(),nullable=False)
    region = db.Column(db.String())
    price_range = db.Column(db.String())
    cuisine = db.Column(db.String(), default='tbc')
    
    # the id pulled from the users table and is shown in restaurants table as user_id in db
    # user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # these releationships are used to pull data from other tables
    # reviews will be shown in a list when restaurant is called
    # the number of users who haved saved the restaurant will be shown in a list when restaurant is called
    reviews = db.relationship('Review', back_populates='restaurant', cascade='all, delete')
    saved = db.relationship('Saved', back_populates='restaurant', cascade='all, delete')


class RestaurantSchema(ma.Schema):
    reviews = fields.List(fields.Nested('ReviewSchema', only=['id','user','rating','message','date' ]))
    # saved = fields.List(fields.Nested('SavedSchema', only=['id','tag']))
    region = fields.String(
        validate=OneOf(VALID_REGION))
    name = fields.String(required=True, validate=And(
        Length(min=1, error='Name must be at least 1 character long'),
        Regexp('^[a-zA-Z0-9 ]+$', error='Name must be alphanumeric')
        ))
    price_range = fields.String(validate=OneOf(VALID_PRICE_RANGE))
    saves = fields.Function(lambda obj: len(obj.saved))

    #average rating from reviews, rounded to 2 decimal places
    avg_rating = fields.Function(lambda obj: round(sum([review.rating for review in obj.reviews])/len(obj.reviews),2) if len(obj.reviews) > 0 else 0)

 
    class Meta:
        fields = ('id', 'name', 'region', 'price_range','cuisine','avg_rating', 'reviews', 'saves', )
        ordered = True