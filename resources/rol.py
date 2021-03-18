from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required

# Models
from models.rol import RolModel

class Rol(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('rol',
        type=str,
        required=True,
        help='El campo nombre no puede estar vacio'
    )

    @jwt_required()
    def get(self, _id):
        rol = RolModel.find_by_id(_id)
        if rol:
            return rol.json(), 200
        return {'message': 'Rol no encontrado'}, 404

    @jwt_required()
    def post(self):
        data = Rol.parser.parse_args()
        if RolModel.find_by_name(data['rol']):
            return {'message': 'Ya existe un rol {}'.format(data['rol'])}, 400

        rol = RolModel(rol=data['rol'])

        try:
            rol.save_to_db()
        except:
            return {'message': 'Ocurrio un error al tratar de crear rol'}, 500

        return rol.json(), 201

    @jwt_required()
    def put(self, _id):
        updated_rol = Rol.parser.parse_args()
        rol = RolModel.find_by_id(_id)

        if rol is None:
            rol = RolModel(updated_rol)
        else:
            rol.rol = updated_rol['rol']
        
        try:
            rol.save_to_db()
        except:
            return {'message': 'Ocurrio un error al tratar de actualizar el rol'}, 500

        return rol.json(), 201

    @jwt_required()
    def delete(self, _id):
        rol = RolModel.find_by_id(_id)
        if rol:
            try:
                rol.delete_from_db()
            except:
                return {'message': 'Ocurrio un error al tratar de eliminar el rol'}, 500
        
        return {'message': 'Rol eliminado exitosamente'}, 200

 
class RolList(Resource):
    @jwt_required()
    def get(self):
        return {'roles': [rol.json() for rol in RolModel.find_all()]}, 200
        
