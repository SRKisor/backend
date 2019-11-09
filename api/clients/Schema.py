from api import ma
from api.clients.models import Clients


class ClientsSchema(ma.ModelSchema):
    """
        Scheme for Clients Model
    """

    class Meta:
        model = Clients


client_schema = ClientsSchema(many=False)
clients_schema = ClientsSchema(many=True)
