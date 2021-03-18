from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required

# Models
from models.store import StoreModel
from models.store_product import StoreProductModel

class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
        type=str,
        required=True,
        help='El campo nombre no puede estar vacio'
    )
    parser.add_argument('address',
        type=str,
        required=True,
        help='El campo direccion no puede estar vacio'
    )
    parser.add_argument('mail',
        type=str,
        required=True,
        help='El campo correo no puede estar vacio'
    )
    parser.add_argument('phone',
        type=str,
        required=True,
        help='El campo telefono no puede estar vacio'
    )

    @jwt_required()
    def get(self, _id):
        store = StoreModel.find_by_id(_id)
        if store:
            return store.json()
        return {'message': 'Tienda no encontrada'}, 404

    @jwt_required()
    def post(self):
        data = Store.parser.parse_args()
        if StoreModel.find_by_name(data['name']):
            return {'message': 'Ya existe una tienda con nombre {}'.format(data['name'])}, 400
        
        store = StoreModel(**data)

        try:
            store.save_to_db()
        except:
            return {'message': 'Ocurrio un error al tratar de crear tienda'}, 500
        
        return store.json(), 201

    @jwt_required()
    def put(self, _id):
        data = Store.parser.parse_args()
        store = StoreModel.find_by_id(_id)

        if store is None:
            store = StoreModel(**data)
        else:
            store.name = data['name']
            store.address = data['address']
            store.mail = data['mail']
            store.phone = data['phone']

        try:
            store.save_to_db()
        except:
            return {'message': 'Ocurrio un error al tratar de actualizar tienda'}, 500
        
        return store.json(), 201

    @jwt_required()
    def delete(self, _id):
        store = StoreModel.find_by_id(_id)

        if store:
            try:
                store.delete_from_db()
            except:
                return {'message': 'Ocurrio un error al tratar de eliminar tienda'}, 500

        return {'message': 'Tienda eliminada exitosamente'}, 200


class StoreList(Resource):
    @jwt_required()
    def get(self):
        return {'stores': [store.json() for store in StoreModel.find_all()]}


class StoreProduct(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('store_id',
        type=int,
        required=True,
        help='El campo store_id no puede estar vacio'
    )
    parser.add_argument('product_id',
        type=int,
        required=True,
        help='El campo product_id no puede estar vacio'
    )
    parser.add_argument('stock',
        type=str,
        required=True,
        help='El campo stock no puede estar vacio'
    )

    @jwt_required()
    def get(self, _id):        
        store_product = StoreProductModel.find_by_id(_id)
        if store_product:
            return store_product.json(), 200
        return {'message': 'Producto en tienda no encontrado'}, 404

    @jwt_required()
    def post(self):
        data = StoreProduct.parser.parse_args()
        response = StoreProductModel.find_by_composite_id(data['store_id'], data['product_id'])
        if response:
            print(data)
            print(response)
            return {'message': 'Ya existe un producto con el id {} en la tienda {}'.format(data['product_id'],data['store_id'])}
        
        store_product = StoreProductModel(**data)

        try:
            store_product.save_to_db()
        except:
            return {'message': 'Ocurrio un error al tratar de guardar el producto'}, 500
        
        return store_product.json()


class StoreProductList(Resource):
    @jwt_required()
    def get(self):
        return {'products': [store_product.json() for store_product in StoreProductModel.find_all()]}, 200