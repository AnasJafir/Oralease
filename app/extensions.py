# app/extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

# Initialisation des extensions sans l'application (Lazy loading)
db = SQLAlchemy()
jwt = JWTManager()
ma = Marshmallow()
migrate = Migrate()