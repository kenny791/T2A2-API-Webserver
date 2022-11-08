# from init import db, ma
# from marshmallow import fields, validates
# from marshmallow.validate import Length, OneOf, And, Regexp
# from marshmallow.exceptions import ValidationError



# class Star(db.Model):
#     __tablename__ = 'stars'

#     id = db.Column(db.Integer,primary_key=True)
#     stars_given = db.Column(db.String(50), nullable=False)


#     review = db.relationship("Review", back_populates='stars')


# class StarSchema(ma.Schema):
#     review = fields.Nested('ReviewSchema', only=('id', 'review_text', 'user', 'restaurant'))
#     user = fields.Nested('UserSchema', only=('id', 'username'))
#     restaurant = fields.Nested('RestaurantSchema', only=('id', 'name'))

#     class Meta:
#         fields = ('id', 'stars_given')
#         ordered = True