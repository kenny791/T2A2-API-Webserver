# from init import db, ma
# from marshmallow import fields

# class Review(db.Model):
#     __tablename__ = 'reviews'

#     id = db.Column(db.Integer, primary_key=True)
#     message = db.Column(db.Text)
#     # rating = db.Column(db.Integer)
#     # date = db.Column(db.Date) #Date created

#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)

#     user = db.relationship ("User", back_populates='Reviews')
#     restaurants = db.relationship ("Restaurant", back_populates='Reviews')

# class ReviewSchema(ma.Schema):
#     user = fields.Nested('UserSchema', only=['username', 'email'])
#     restaurant = fields.Nested('RestaurantSchema')

#     class Meta:
#         fields = ('id', 'message', 'user', 'restaurant')
#         ordered = True