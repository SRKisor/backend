from flask import jsonify, request
from flask.views import MethodView
from werkzeug.exceptions import abort
from sqlalchemy import func

from api.database import db_session

from api.items.models import Items
from api.items.Schema import item_schema, items_schema

from api.helpers import response


class ItemsAPI(MethodView):
    def get(self, item_code):
        if item_code is None:
            items = Items.query.all()

            report = Items.query.with_entities(func.date_trunc("day", Items.created_at).label("date"), func.count(
                Items.item_code).label("count")).group_by(func.date_trunc("day", Items.created_at)).all()

            return jsonify(data=items_schema.dump(items), report=report)
        else:
            item = Items.query.filter(Items.item_code == item_code).first()

            if not item:
                return response('Not Found', f'Item with Item Code {item_code} is not available.', 404)

            return item_schema.jsonify(item)

    def post(self):
        if not request.content_type == 'application/json':
            return response('Failed', 'Content-type must be application/json', 401)

        data = request.get_json()

        fields = ['item_code', 'name', 'qty', 'retail_price',
            'wholesale_price', 'mfd_date', 'exp_date']
        string = ''

        for i in fields:
            if not data.get(f'{i}'):
                string = string+f'\"{i}\", '

        if string:
            return response('Invalid POST Request', f'These fields should be included in the POST Request. {string}', 404)

        item = Items(
            item_code=data.get('item_code'),
            name=data.get('name'),
            qty=data.get('qty'),
            retail_price=data.get('retail_price'),
            wholesale_price=data.get('wholesale_price'),
            mfd_date=data.get('mfd_date'),
            exp_date=data.get('exp_date')
        )

        db_session.add(item)
        db_session.commit()

        return response('Added Successfully.', f'Successfully added the item with Item Code {str(item.item_code)}', 200, item_schema.dump(item))

    def delete(self, item_code):

        item = Items.query.filter(Items.item_code == item_code).first()

        if not item:
            return response('Not Found', f'Item with Item Code {item_code} is not available.', 404)

        db_session.delete(item)
        db_session.commit()

        return response('Delete Successful.', f'Successfully deleted the Items with Item Code {str(item_code)}', 200, item_schema.dump(item))

    def put(self, item_code):
        if not request.content_type == 'application/json':
            return response('failed', 'Content-type must be application/json', 401)

        item = Items.query.filter(Items.item_code == item_code).first()

        if not item:
            return response('Not Found', f'Item with Item Code {item_code} is not available.', 404)

        data = request.get_json()

        if data.get("name"):
            item.name = data.get('name')

        if data.get("qty"):
            item.qty = data.get('qty')

        if data.get("retail_price"):
                    item.retail_price = data.get('retail_price')

        if data.get("wholesale_price"):
                    item.wholesale_price = data.get('wholesale_price')

        if data.get("mfd_date"):
                    item.mfd_date = data.get('mfd_date')

        if data.get("exp_date"):
                    item.exp_date = data.get('exp_date')

        db_session.commit()

        return response('Update Successful.', f'Successfully updated the Items with Item Code {str(item_code)}', 200,item_schema.dump(item))
