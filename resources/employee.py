from flask_restful import Resource, reqparse

# Models
from models.employee import EmployeeModel

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

    def post(self, dni):
        if EmployeeModel.find_by_dni(dni):
            return {'message': 'Ya existe un empleado con cedula {}'.format(dni)}, 400
        
        data = Employee.parser.parse_args()
        employee = EmployeeModel(**data, dni)

        try:
            employee.save_to_db()
        except:
            return {'message': 'Ocurrio un error al tratar de crear empleado'}, 500
        
        return employee.json(), 201

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
    def get(self):
        return {'employees': [employee.json() for employee in EmployeeModel.find_all()]}