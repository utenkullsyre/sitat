from flask import request
from flask_restful import Resource
from Model import db, Barn, BarnSchema

barns_schema = BarnSchema(many=True)
barn_schema = BarnSchema()

class BarnResource(Resource):
    def get(self):
        barns = Barn.query.all()
        barns = barns_schema.dump(barns).data
        return {'status': 'success', 'data': barns}, 200

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = barn_schema.load(json_data)
        if errors:
            return errors, 422
        barn = Barn.query.filter_by(navn=data['navn']).first()
        if barn:
            return {'message': 'Barn eksisterer allerede'}, 400

        barn = Barn(data['navn'])


        db.session.add(barn)
        db.session.commit()
        #
        result = barn_schema.dump(barn).data

        return { "status": 'success', 'data': result }, 201

    def put(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = barn_schema.load(json_data)
        if errors:
            return errors, 422
        barn = Barn.query.filter_by(id=json_data['id']).first()
        if not barn:
            return {'message': 'Barn eksisterer ikke'}, 400
        barn.navn = data['navn']
        db.session.commit()

        result = barn_schema.dump(barn).data

        return { "status": 'success', 'data': result }, 204

    def delete(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = barn_schema.load(json_data)
        if errors:
            return errors, 422
        barn = Barn.query.filter_by(id=data['id']).delete()
        db.session.commit()

        result = barn_schema.dump(sitat).data

        return { "status": 'success', 'data': result}, 204
