from flask import jsonify, request
from flask.views import MethodView
from werkzeug.exceptions import abort

from api.database import db_session

from api.distributors.models import Distributors
from api.distributors.Schema import distributor_schema, distributors_schema
from api.helpers import response


class DistributorsAPI(MethodView):

    def get(self, id):
        if id is None:
            distributors = Distributors.query.all()
            return distributors_schema.jsonify(distributors)
        else:
            distributor = Distributors.query.filter(
                Distributors.id_ == id).first()

            if not distributor:
                abort(404)

            return distributor_schema.jsonify(distributor)

    def post(self):
        if not request.content_type == 'application/json':
            return response('failed', 'Content-type must be application/json', 401)

        data = request.get_json()

        distributors = Distributors(
            name=data.get('name'),
            address=data.get('address'),
            telephone=data.get('telephone'),
            email=data.get('email')
        )

        db_session.add(distributors)
        db_session.commit()

        distributor = Distributors.query.filter(
            Distributors.name == data.get('name')).first()

        return distributor_schema.jsonify(distributor)

    def delete(self, id):
        if not request.content_type == 'application/json':
            return response('failed', 'Content-type must be application/json', 401)

        distributor = Distributors.query.filter(Distributors.id_ == id).first()

        if not distributor:
            abort(404)

        db_session.delete(distributor)
        db_session.commit()

        return response('success', 'Successfully deleted the item from Distributors with Id ' + str(id), 200)

    def put(self, id):
        if not request.content_type == 'application/json':
            return response('failed', 'Content-type must be application/json', 401)

        distributor = Distributors.query.filter(Distributors.id_ == id).first()

        if not distributor:
            abort(404)

        data = request.get_json()

        distributor.name = data.get('name'),
        distributor.address = data.get('address'),
        distributor.telephone = data.get('telephone'),
        distributor.email = data.get('email')

        db_session.commit()

        return response('success', 'Successfully updated the item from Distributors with Id ' + str(id), 200)
