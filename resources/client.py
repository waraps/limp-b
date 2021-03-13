from flask_restful import Resource, reqparse

# Models
from models.client import ClientModel

class Client(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
        type=str,
        required=True,
        help='El campo nombre no puede estar vacio'
    )
    parser.add_argument('lastname',
        type=str,
        required=True,
        help='El campo apellido no puede estar vacio'
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
    parser.add_argument('dni',
        type=str,
        required=True,
        help='El campo cedula no puede estar vacio'
    )

    def get(self, _id):
        client = ClientModel.find_by_id(_id)
        if client:
            return client.json()
        return {'message': 'Cliente no encontrado'}, 404

    def post(self):
        data = Client.parser.parse_args()
        if ClientModel.find_by_dni(data['dni']):
            return {'message': 'Ya existe un cliente con cedula {}'.format(data['dni'])}, 400
        
        client = ClientModel(**data)

        try:
            client.save_to_db()
        except:
            return {'message': 'Ocurrio un error al tratar de crear cliente'}, 500
        
        return client.json(), 201

    def put(self, _id):
        data = Client.parser.parse_args()
        client = ClientModel.find_by_id(_id)

        if client is None:
            client = ClientModel(**data)
        else:
            client.name = data['name']
            client.lastname = data['lastname']
            client.mail = data['mail']
            client.phone = data['phone']
            client.dni = data['dni']

        try:
            client.save_to_db()
        except:
            return {'message': 'Ocurrio un error al tratar de actualizar cliente'}, 500
        
        return client.json(), 201

    def delete(self, _id):
        client = ClientModel.find_by_id(_id)

        if client:
            try:
                client.delete_from_db()
            except:
                return {'message': 'Ocurrio un error al tratar de eliminar cliente'}, 500

        return {'message': 'Cliente eliminado exitosamente'}, 200


class ClientList(Resource):
    def get(self):
        return {'clients': [client.json() for client in ClientModel.find_all()]}