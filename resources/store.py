from flask_restful import Resource, reqparse

# Models
from models.store import StoreModel

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

    def get(self, _id):
        store = StoreModel.find_by_id(_id)
        if store:
            return store.json()
        return {'message': 'Tienda no encontrada'}, 404

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

    def delete(self, _id):
        store = StoreModel.find_by_id(_id)

        if store:
            try:
                store.delete_from_db()
            except:
                return {'message': 'Ocurrio un error al tratar de eliminar tienda'}, 500

        return {'message': 'Tienda eliminada exitosamente'}, 200


class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.find_all()]}