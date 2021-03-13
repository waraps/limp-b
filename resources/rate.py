from flask_restful import Resource, reqparse

# Models
from models.rate import RateModel

class Rate(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('rate',
        type=float,
        required=True,
        help='El campo tasa no puede estar vacio'
    )
    def get(self, _id):
        rate = RateModel.find_by_id(_id)
        if rate:
            return rate.json(), 200
        return {'message': 'tasa no encontrada'}, 404

    def post(self):
        data = Rate.parser.parse_args()
        rate = RateModel(**data)

        try:
            rate.save_to_db()
        except:
            return {'message': 'Ocurrio un error al tratar de crear rol'}, 500

        return rate.json(), 201

 
class RateList(Resource):
    def get(self):
        return {'rates': [rate.json() for rate in RateModel.find_all()]}, 200
        
