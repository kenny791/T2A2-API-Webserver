from init import db, ma
from marshmallow import fields, validates
from marshmallow.validate import Length, OneOf, And, Regexp
from marshmallow.exceptions import ValidationError



class Rating(db.Model):
    __tablename__ = 'ratings'
    id = db.Column(db.Integer,primary_key=True)
    rating = db.Column(db.Integer, nullable=False)

    review_id = db.Column(db.Integer, 

    reviews = db.relationship('Review', back_populates='rating')