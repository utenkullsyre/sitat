from flask import request
from flask_restful import Resource
from Model import db, Sitat, SitatSchema

# TODO: Fjern alle 204 koder da disse fører til en valueerror. Endre de til 200

sitater_schema = SitatSchema(many=True)
sitat_schema = SitatSchema()

class SitatResource(Resource):
    def get(self):
        sitater = Sitat.query.all()
        sitater = sitater_schema.dump(sitater).data
        return {'status': 'success', 'data': sitater}, 200

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # return json_data
        # Validate and deserialize input
        data, errors = sitat_schema.load(json_data)
        if errors:
            return errors,400
        sitat = Sitat.query.filter_by(sitat=data['sitat']).first()
        if sitat:
            return {'message': 'Sitat eksisterer allerede'}, 400

        sitat = Sitat(data['sitat'], int(data['barn_id']), int(data['humoer_id']), data['info'])


        db.session.add(sitat)
        # return str(sitat.__dict__)
        db.session.commit()
        #
        result = sitat_schema.dump(sitat).data

        return { "status": 'success', 'data': result }, 201

    def put(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = sitat_schema.load(json_data)
        if errors:
            return errors, 422
        sitat = Sitat.query.filter_by(id=json_data['id']).first()
        if not sitat:
            return {'message': 'Sitat eksisterer ikke'}, 400
        sitat.sitat = data['sitat']
        db.session.commit()

        result = sitat_schema.dump(sitat).data

        return { "status": 'success', 'data': result }, 204


    def delete(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400

        sitat = Sitat.query.filter_by(id=json_data['id']).delete()
        db.session.commit()

        result = sitat_schema.dump(sitat).data

        return { "status": 'success', 'data': result},200
