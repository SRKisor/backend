from api import ma
from api.bill.models import Bills


class BillsSchema(ma.ModelSchema):
    """
        Scheme for Bills Model
    """

    class Meta:
        model = Bills

    client_name = ma.Function(lambda obj: obj.client.name)


bill_schema = BillsSchema(many=False)
bills_schema = BillsSchema(many=True)
