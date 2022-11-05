from init import db, ma
from marshmallow import fields

class Restaurant(db.Model):
    __tablename__ = 'restaurants'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(),nullable=False)
    address = db.Column(db.String())
    is_vegan = db.Column(db.Boolean())
    price_range = db.Column(db.String())
    
    # the id pulled from the users table and is shown in restaurants table as user_id in db
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # object is what is shown on the client side
    added_by = db.relationship('User', back_populates='restaurants_submitted')
    reviews = db.relationship('Review', back_populates='restaurant', cascade='all, delete')


class RestaurantSchema(ma.Schema):
    added_by = fields.Nested('UserSchema', only=['username'])
    reviews = fields.List(fields.Nested('ReviewSchema', only=['user','rating','date', 'message']))
    class Meta:
        fields = ('id', 'name', 'address', 'is_vegan', 'price_range', 'added_by', 'reviews')
        ordered = True