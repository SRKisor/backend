from flask import jsonify, request
from flask.views import MethodView
from werkzeug.exceptions import abort

from api.database import db_session

from api.clients.models import Clients
from api.clients.Schema import client_schema, clients_schema
from api.helpers import response


class ClientsAPI(MethodView):
    """
        class for "/clients/" endpoint
    """

    def get(self, id):
        """function for "GET /clients/" endpoint

        Args:
            id (int): id for the Client

        Returns:
            If endpoint is "GET /clients/<id>"
                {
                    "address": "Address 1",
                    "created_at": "2019-09-20T06:07:23.611071",
                    "email": "admin@admin.com",
                    "id_": 1,
                    "name": "Client 1",
                    "telephone": "123456789",
                    "updated_at": null
                }

            If endpoint is "GET /clients/"
                [
                    {
                        "address": "Address 1",
                        "created_at": "2019-09-20T06:07:23.611071",
                        "email": "admin@admin.com",
                        "id_": 1,
                        "name": "Client 1",
                        "telephone": "123456789",
                        "updated_at": null
                    },
                    {
                        "address": "Address 2",
                        "created_at": "2019-09-20T06:07:23.614419",
                        "email": "admin@admin.com",
                        "id_": 2,
                        "name": "Client 2",
                        "telephone": "123456789",
                        "updated_at": null
                    }
                ]
        """

        if id is None:
            clients = Clients.query.all()
            return clients_schema.jsonify(clients)
        else:
            client = Clients.query.filter(
                Clients.id_ == id).first()

            if not client:
                abort(404)

            return client_schema.jsonify(client)

    def post(self):
        """function for "POST /clients/" endpoint

        Returns:
            {
                "address": "Address 1",
                "created_at": "2019-09-20T06:07:23.611071",
                "email": "admin@admin.com",
                "id_": 1,
                "name": "Client 1",
                "telephone": "123456789",
                "updated_at": null
            }
        """

        if not request.content_type == 'application/json':
            return response('failed', 'Content-type must be application/json', 401)

        data = request.get_json()

        clients = Clients(
            name=data.get('name'),
            address=data.get('address'),
            telephone=data.get('telephone'),
            email=data.get('email')
        )

        db_session.add(clients)
        db_session.commit()

        client = Clients.query.filter(
            Clients.name == data.get('name')).first()

        return client_schema.jsonify(client)

    def delete(self, id):
        """function for "DELETE /clients/<id>" endpoint

        Args:
            id (int): id for the Client

        Returns:
            {
                "status" : "success,
                "message" : "Successfully deleted the item from Clients with Id 1"
            }
        """

        if not request.content_type == 'application/json':
            return response('failed', 'Content-type must be application/json', 401)

        client = Clients.query.filter(Clients.id_ == id).first()

        if not client:
            abort(404)

        db_session.delete(client)
        db_session.commit()

        return response('success', 'Successfully deleted the item from Client with Id ' + str(id), 200)

    def put(self, id):
        """function for "PUT /clients/<id>" endpoint

        Args:
            id (int): id for the Client

        Returns:
            {
                "status" : "success,
                "message" : "Successfully updated the item from Clients with Id 1"
            }
        """

        if not request.content_type == 'application/json':
            return response('failed', 'Content-type must be application/json', 401)

        client = Clients.query.filter(Clients.id_ == id).first()

        if not client:
            abort(404)

        data = request.get_json()

        client.name = data.get('name'),
        client.address = data.get('address'),
        client.telephone = data.get('telephone'),
        client.email = data.get('email')

        db_session.commit()

        return response('success', 'Successfully updated the item from Clients with Id ' + str(id), 200)
