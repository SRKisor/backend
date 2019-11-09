from api import ma
from api.distributors.models import Distributors


class DistributorsSchema(ma.ModelSchema):
    class Meta:
        model = Distributors


distributor_schema = DistributorsSchema(many=False)
distributors_schema = DistributorsSchema(many=True)
