import os
from datetime import timedelta

from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager
from db import db
from flask_migrate import Migrate

# Resources
from resources.rol import Rol, RolList
from resources.employee import Employee, EmployeeList
from resources.store import Store, StoreList, StoreProduct, StoreProductList
from resources.product import Product, ProductList
from resources.client import Client, ClientList
from resources.invoice import Invoice, InvoiceList
from resources.rate import Rate, RateList

app = Flask(__name__)

# Configs
app.config['SECRET_KEY'] = os.environ.get('API_SECRET_KEY')
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

CORS(app)
api = Api(app)
jwt = JWTManager(app)
db.init_app(app)
migrate = Migrate(app, db, render_as_batch=True)

# Routes
api.add_resource(Rol, '/api/v2/rol/<int:_id>', '/api/v2/rol')
api.add_resource(RolList, '/api/v2/roles')

api.add_resource(Store, '/api/v2/store/<int:_id>', '/api/v2/store')
api.add_resource(StoreList, '/api/v2/stores')

api.add_resource(Product, '/api/v2/product/<int:_id>', '/api/v2/product')
api.add_resource(ProductList, '/api/v2/products')

api.add_resource(StoreProduct, '/api/v2/store/product/<int:_id>', '/api/v2/store/product')
api.add_resource(StoreProductList, '/api/v2/store/products')

api.add_resource(Employee, '/api/v2/employee/<int:_id>', '/api/v2/employee')
api.add_resource(EmployeeList, '/api/v2/employees')

api.add_resource(Client, '/api/v2/client/<int:_id>', '/api/v2/client')
api.add_resource(ClientList, '/api/v2/clients')

api.add_resource(Rate, '/api/v2/rate/<int:_id>', '/api/v2/rate')
api.add_resource(RateList, '/api/v2/rates')

api.add_resource(Invoice, '/api/v2/invoice/<int:_id>', '/api/v2/invoice')
api.add_resource(InvoiceList, '/api/v2/invoices')

if __name__ == '__main__':
    app.run(
        port=os.environ.get('PORT'), 
        debug=True
    )
