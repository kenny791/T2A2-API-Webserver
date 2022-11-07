from init import db,ma
from marshmallow import fields
from marshmallow.validate import Email, OneOf, And, Regexp, Length
from marshmallow.exceptions import ValidationError


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    is_admin = db.Column(db.Boolean(), default=False)

    # object is what is shown on the client side
    reviews_submitted = db.relationship('Review', back_populates='user', cascade='all, delete')

class UserSchema(ma.Schema):
    restaurants_submitted = fields.List(fields.Nested('RestaurantSchema', only=['name']))
    reviews_submitted = fields.List(fields.Nested('ReviewSchema', only=['restaurant','rating','date','message']))
    # input fields area validated by marshmallow
    email =fields.String(validate=Email())
    username = fields.String(validate=And(
        Length(min=1, error='Username must be at least 1 character long'),
        Length(max=50, error='Username must be less than 50 characters long'),
        Regexp('^[a-zA-Z0-9 ]+$', error='Username must be alphanumeric')
        ))
    password = fields.String(validate=Length(min=6, error='Password must be at least 6 characters long'))
    class Meta:
        fields = ('id', 'username', 'email', 'password', 'is_admin', 'restaurants_submitted', 'reviews_submitted')
        ordered = True