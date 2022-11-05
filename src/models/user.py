from init import db,ma
from marshmallow import fields

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    is_admin = db.Column(db.Boolean(), default=False)

    # object is what is shown on the client side
    restaurants_submitted = db.relationship('Restaurant', back_populates='added_by', cascade='all, delete')
    reviews_submitted = db.relationship('Review', back_populates='user', cascade='all, delete')

class UserSchema(ma.Schema):
    restaurants_submitted = fields.List(fields.Nested('RestaurantSchema', only=['name']))
    reviews_submitted = fields.List(fields.Nested('ReviewSchema', only=['restaurant','message']))

    class Meta:
        fields = ('id', 'username', 'email', 'password', 'is_admin', 'restaurants_submitted', 'reviews_submitted')
        ordered = True