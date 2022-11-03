from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

#SQLAlchemy is used to interact with the database
db = SQLAlchemy()
#Marshmallow is a library for converting complex datatypes, such as objects, to and from native Python datatypes.
ma = Marshmallow()
