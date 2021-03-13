from flask_restful import Resource, reqparse

# Models
from models.invoice import InvoiceModel

class Invoice(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('mount',
        type=float,
        required=True,
        help='El campo monto no puede estar vacio'
    )
    parser.add_argument('code',
        type=str,
        required=True,
        help='El campo codigo no puede estar vacio'
    )
    parser.add_argument('status',
        type=bool,
        required=True,
        help='El campo status no puede estar vacio'
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help='El campo store_id no puede estar vacio'
    )
    parser.add_argument('employee_id',
        type=int,
        required=True,
        help='El campo employee_id no puede estar vacio'
    )
    parser.add_argument('rate_id',
        type=int,
        required=True,
        help='El campo rate_id no puede estar vacio'
    )

    def get(self, _id):
        invoice = InvoiceModel.find_by_id(_id)
        if invoice:
            return invoice.json()
        return {'message': 'Factura no encontrada'}, 404

    def post(self):
        data = Invoice.parser.parse_args()
        if InvoiceModel.find_by_code(data['code']):
            return {'message': 'Ya existe un factura con codigo {}'.format(data['code'])}, 400
        
        invoice = InvoiceModel(**data)

        try:
            invoice.save_to_db()
        except:
            return {'message': 'Ocurrio un error al tratar de crear factura'}, 500
        
        return invoice.json(), 201

    def put(self, _id):
        data = Invoice.parser.parse_args()
        invoice = InvoiceModel.find_by_id(_id)

        if invoice is None:
            invoice = InvoiceModel(**data)
        else:
            invoice.mount = data['mount']
            invoice.code = data['code']
            invoice.status = data['status']

        try:
            invoice.save_to_db()
        except:
            return {'message': 'Ocurrio un error al tratar de actualizar factura'}, 500
        
        return invoice.json(), 201

    def delete(self, _id):
        invoice = InvoiceModel.find_by_id(_id)

        if invoice:
            try:
                invoice.delete_from_db()
            except:
                return {'message': 'Ocurrio un error al tratar de eliminar factura'}, 500

        return {'message': 'Factura eliminada exitosamente'}, 200


class InvoiceList(Resource):
    def get(self):
        return {'invoices': [invoice.json() for invoice in InvoiceModel.find_all()]}