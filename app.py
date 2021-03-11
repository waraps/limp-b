from flask import Flask
from flask_restful import Api
from db import db
from flask_migrate import Migrate

from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'jwtsecretkey'

db.init_app(app)
db.app = app
api = Api(app)

Migrate(app, db)

api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == "__main__":
    app.run(port=5000, debug=True)
