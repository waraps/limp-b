import os
from datetime import timedelta

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from db import db

# Resources
# imports here

app = Flask(__name__)

# Configs
app.config['SECRET_KEY'] = os.environ.get('API_SECRET_KEY')
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

db.init_app(app)
api = Api(app)
jwt = JWTManager(app)

# Routes
# here

if __name__ == '__main__':
    app.run(
        port=os.environ.get('PORT'), 
        debug=os.environ.get('DEBUG')
    )