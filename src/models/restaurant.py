from main import db

class Restaurant(db.Model):
    # the table name for the db
    __tablename__= "restaurants"

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String())
    address = db.Column(db.String())
    is_vegan = db.Column(db.Boolean())
    price_range = db.Column(db.String())