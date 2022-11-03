from main import db, ma

class Restaurant(db.Model):
    __tablename__ ='restaurants'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(),nullable=False)
    address = db.Column(db.String())
    is_vegan = db.Column(db.Boolean())
    price_range = db.Column(db.String())


class RestaurantSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'address', 'is_vegan', 'price_range')
        ordered = True