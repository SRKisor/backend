from api import ma
from api.items.models import Items


class ItemsSchema(ma.ModelSchema):
    class Meta:
        model = Items


item_schema = ItemsSchema(many=False)
items_schema = ItemsSchema(many=True)
