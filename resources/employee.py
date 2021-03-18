from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token, 
    get_jwt_identity,
    jwt_required,
    get_jwt
)

# Models
from models.employee import EmployeeModel

class EmployeeRegister(Resource):
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
    parser.add_argument('password',
        type=str,
        required=True,
        help='El campo contrasena no puede estar vacio'
    )
    parser.add_argument('rol_id',
        type=int,
        required=True,
        help='El campo rol_id no puede estar vacio'
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help='El campo store_id no puede estar vacio'
    )

    def post(self):
        data = Employee.parser.parse_args()
        if EmployeeModel.find_by_dni(data['dni']):
            return {'message': 'Ya existe un empleado con cedula {}'.format(data['dni'])}, 400
        
        data['password'] = generate_password_hash(data['password'])
        employee = EmployeeModel(**data)

        try:
            employee.save_to_db()
        except:
            return {'message': 'Ocurrio un error al tratar de crear empleado'}, 500
        
        return employee.json(), 201


class EmployeeLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('mail',
        type=str,
        required=True,
        help='El campo correo no puede estar vacio'
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help='El campo contrasena no puede estar vacio'
    )

    def post(self):
        data = EmployeeLogin.parser.parse_args()

        employee = EmployeeModel.find_by_mail(data['mail'])

        if employee and check_password_hash(employee.password, data['password']):
            access_token = create_access_token(identity=employee.id, fresh=True)
            refresh_token = create_refresh_token(employee.id)
            return {
                'employee': employee.json(),
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        
        return {'message': 'Invalid credentials'}, 401


class EmployeeLogout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        # BLACKLIST.add(jti)
        return {'message': 'Successfully logged out.'}, 200


class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_employee = get_jwt_identity()
        new_token = create_access_token(identity=current_employee, fresh=False)
        return {'access_token': new_token}, 200

class Employee(Resource):
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
    parser.add_argument('password',
        type=str,
        required=True,
        help='El campo contrasena no puede estar vacio'
    )
    parser.add_argument('rol_id',
        type=int,
        required=True,
        help='El campo rol_id no puede estar vacio'
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help='El campo store_id no puede estar vacio'
    )

    def get(self, _id):
        employee = EmployeeModel.find_by_id(_id)
        if employee:
            return employee.json()
        return {'message': 'Empleado no encontrado'}, 404

    def put(self, _id):
        data = Employee.parser.parse_args()
        employee = EmployeeModel.find_by_id(_id)

        if employee is None:
            employee = EmployeeModel(**data)
        else:
            employee.name = data['name']
            employee.lastname = data['lastname']
            employee.mail = data['mail']
            employee.phone = data['phone']
            employee.dni = data['dni']

        try:
            employee.save_to_db()
        except:
            return {'message': 'Ocurrio un error al tratar de actualizar empleado'}, 500
        
        return employee.json(), 201

    def delete(self, _id):
        employee = EmployeeModel.find_by_id(_id)

        if employee:
            try:
                employee.delete_from_db()
            except:
                return {'message': 'Ocurrio un error al tratar de eliminar empleado'}, 500

        return {'message': 'Empleado eliminado exitosamente'}, 200


class EmployeeList(Resource):
    @jwt_required()
    def get(self):
        return {'employees': [employee.json() for employee in EmployeeModel.find_all()]}