from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required

# Models
from models.product import ProductModel

class Product(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
        type=str,
        required=True,
        help='El campo nombre no puede estar vacio'
    )
    parser.add_argument('price',
        type=float,
        required=True,
        help='El campo precio no puede estar vacio'
    )

    @jwt_required()
    def get(self, _id):
        product_id = ProductModel.find_by_id(_id)
        if product_id:
            return product_id.json(), 200
        return {'message': 'Producto no encontrado'}, 404

    @jwt_required()
    def post(self):
        data = Product.parser.parse_args()
        if ProductModel.find_by_name(data['name']):
            return {'message': 'Ya existe un producto con el nombre {}'.format(data['name'])}, 400

        product = ProductModel(**data)

        try:
            product.save_to_db()
        except:
            return {'message': 'Ocurrio un error al tratar de crear rol'}, 500

        return product.json(), 201

    @jwt_required()
    def put(self, _id):
        updated_product = Product.parser.parse_args()
        product = ProductModel.find_by_id(_id)

        if product is None:
            product = ProductModel(updated_product)
        else:
            product.name = updated_rol['name']
            product.price = updated_rol['price']
        
        try:
            product.save_to_db()
        except:
            return {'message': 'Ocurrio un error al tratar de actualizar el producto'}, 500

        return product.json(), 201

    @jwt_required()
    def delete(self, _id):
        product = ProductModel.find_by_id(_id)
        if product:
            try:
                product.delete_from_db()
            except:
                return {'message': 'Ocurrio un error al tratar de eliminar el rol'}, 500
        
        return {'message': 'Rol eliminado exitosamente'}, 200

 
class ProductList(Resource):
    @jwt_required()
    def get(self):
        return {'products': [product.json() for product in ProductModel.find_all()]}, 200
        
