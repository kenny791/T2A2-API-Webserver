from init import db, ma
from marshmallow import fields, validates
from marshmallow.validate import Length, OneOf, And, Regexp
from marshmallow.exceptions import ValidationError

# list of valid data that can inputted into the price_range and Location field
VALID_PRICE_RANGE = ['$', '$$', '$$$', '$$$$']
VALID_LOCATION = ['North', 'South', 'East', 'West']

class Restaurant(db.Model):
    __tablename__ = 'restaurants' 

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    location = db.Column(db.String)
    price_range = db.Column(db.String)
    cuisine = db.Column(db.String(20), default='tbc')
   
    # backpopulating relationships, allows for data to be retrieved from the other tables
    reviews = db.relationship('Review', back_populates='restaurant', cascade='all, delete')
    saved = db.relationship('Saved', back_populates='restaurant', cascade='all, delete')

# marshmallow schema, used to validate data before it is sent to the db, and to format the data before it is sent to the client
class RestaurantSchema(ma.Schema):
        # saved = fields.List(fields.Nested('SavedSchema', only=['id','tag']))
    location = fields.String(
        validate=OneOf(VALID_LOCATION))
    name = fields.String(required=True, validate=And(
        Length(min=1, error='Name must be at least 1 character long'),
        Regexp('^[a-zA-Z0-9 ]+$', error='Name must be alphanumeric')
        ))
    price_range = fields.String(validate=OneOf(VALID_PRICE_RANGE))
    saved_for_later = fields.Function(lambda obj: len(obj.saved))
    tagged_to_go = fields.Function(lambda obj: len([save for save in obj.saved if save.tag == 'To Go']))
    tagged_fave = fields.Function(lambda obj: len([save for save in obj.saved if save.tag == 'Fave']))
    avg_rating = fields.Function(lambda obj: round(sum([review.rating for review in obj.reviews])/len(obj.reviews),2) if len(obj.reviews) > 0 else 0)
    reviews = fields.List(fields.Nested('ReviewSchema', only=['id','user','rating','message','date' ]))

    # the fields that are sent to the client
    class Meta:
        fields = ('id', 'name', 'location', 'price_range','cuisine','avg_rating', 'reviews', 'saved_for_later','tagged_to_go', 'tagged_fave' )
        ordered = True

        