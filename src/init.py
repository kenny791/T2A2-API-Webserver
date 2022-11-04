from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

#SQLAlchemy is used to interact with the database
db = SQLAlchemy()
#Marshmallow is a library for converting complex datatypes, such as objects, to and from native Python datatypes.
ma = Marshmallow()
#Bcrypt is a library for converting passwords to hashes
bcrypt = Bcrypt()
#JWT is a library for creating and verifying JSON Web Tokens
jwt = JWTManager()
