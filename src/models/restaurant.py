from init import db, ma
from marshmallow import fields, validates
from marshmallow.validate import Length, OneOf, And, Regexp
from marshmallow.exceptions import ValidationError

VALID_PRICE_RANGE = ['$', '$$', '$$$', '$$$$']
VALID_REGION = ['North', 'South', 'East', 'West']

class Restaurant(db.Model):
    __tablename__ = 'restaurants'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(),nullable=False)
    region = db.Column(db.String())
    price_range = db.Column(db.String())
    cuisine = db.Column(db.String(), default='tbc')
    
    # the id pulled from the users table and is shown in restaurants table as user_id in db
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # object is what is shown on the client side
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


    @validates('price_range',)
    def validate_price_range(self, v2):
        if v2 == '$$$$':
            raise ValidationError('Vegan restaurants are not that expensive')
    
  


    class Meta:
        fields = ('id', 'name', 'region', 'price_range','cuisine', 'reviews')
        ordered = True