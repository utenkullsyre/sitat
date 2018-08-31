from flask import request
from flask_restful import Resource
from Model import db, Humoer, HumoerSchema

humoers_schema = HumoerSchema(many=True)
humoer_schema = HumoerSchema()

class HumoerResource(Resource):
    def get(self):
        humoers = Humoer.query.all()
        humoers = humoers_schema.dump(humoers).data
        return {'status': 'success', 'data': humoers}, 200

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = humoer_schema.load(json_data)
        if errors:
            return errors, 422
        humoer = Humoer.query.filter_by(navn=data['navn']).first()
        if humoer:
            return {'message': 'Humoer eksisterer allerede'}, 400

        humoer = Humoer(data['navn'])


        db.session.add(humoer)
        db.session.commit()
        #
        result = humoer_schema.dump(humoer).data

        return { "status": 'success', 'data': result }, 201

    def put(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = humoer_schema.load(json_data)
        if errors:
            return errors, 422
        humoer = Humoer.query.filter_by(id=json_data['id']).first()
        if not humoer:
            return {'message': 'Humoer eksisterer ikke'}, 400

        oppsamlingsListe = []
        if 'beskrivelse' in data:
            humoer.beskrivelse = data['beskrivelse']
        if 'navn' in data:
            humoer.navn = data['navn']

        humoer.navn = data['navn']
        db.session.commit()

        result = humoer_schema.dump(humoer).data

        return { "status": 'success', 'data': result }, 204

    def delete(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        humoer = Humoer.query.filter_by(id=json_data['id']).delete()
        db.session.commit()

        result = humoer_schema.dump(humoer).data

        return { "status": 'success', 'data': result}, 204
