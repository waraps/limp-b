from flask_restful import Resource, reqparse

from models.model_test import ModelTest

class ModelTestResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
        type=str,
        required=True,
        help='Campo vacio'
    )

    def post(self):
        data = ModelTestResource.parser.parse_args()

        model_test = ModelTest(data['name'])

        model_test.save_to_db()
        return model_test.json()