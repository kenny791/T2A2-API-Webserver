from init import db, ma
from marshmallow import fields

class Restaurant(db.Model):
    __tablename__ = 'restaurants'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(),nullable=False)
    address = db.Column(db.String())
    is_vegan = db.Column(db.Boolean())
    price_range = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    added_by = db.relationship('User', back_populates='restaurants')


class RestaurantSchema(ma.Schema):
    added_by = fields.Nested('UserSchema', only=('username',))
    class Meta:
        fields = ('id', 'name', 'address', 'is_vegan', 'price_range', 'added_by')
        ordered = True