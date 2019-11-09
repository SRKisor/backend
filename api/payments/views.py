from flask import jsonify, request, make_response
from flask.views import MethodView
from werkzeug.exceptions import abort
from sqlalchemy import update

from api.database import db_session

from api.payments.models import Payments, Payment_Methods, Payment_Types
from api.payments.Schema import payment_schema, payments_schema

from api.helpers import response, require_login


class PaymentsAPI(MethodView):
    # decorators = [require_login]

    def get(self, id):
        if id is None:
            payments = Payments.query.all()

            return payments_schema.jsonify(payments)
        else:
            payment = Payments.query.filter(Payments.id_ == id).first()

            if not payment:
                abort(404)

            return payment_schema.jsonify(payment)

    def post(self):
        if not request.content_type == 'application/json':
            return response('failed', 'Content-type must be application/json', 401)

        data = request.get_json()

        payment_type1 = Payment_Types.query.filter(
            Payment_Types.id_ == data.get('payment_types')).first()

        payment_method1 = Payment_Methods.query.filter(
            Payment_Methods.id_ == data.get('payment_methods')).first()

        payment = Payments(
            amount=data.get('amount'),
            date=data.get('date'),
            due_date=data.get('due_date'),
            paid=data.get('paid'),
            payment_methods=payment_method1,
            payment_types=payment_type1
        )

        db_session.add(payment)
        db_session.commit()

        return payment_schema.jsonify(payment)

    def delete(self, id):
        if not request.content_type == 'application/json':
            return response('failed', 'Content-type must be application/json', 401)

        payment = Payments.query.filter(Payments.id_ == id).first()

        if not payment:
            abort(404)

        db_session.delete(payment)
        db_session.commit()

        return response('success', 'Successfully deleted the item from Payments with Id ' + str(id), 200)

    def put(self, id):
        if not request.content_type == 'application/json':
            return response('failed', 'Content-type must be application/json', 401)

        payment = Payments.query.filter(Payments.id_ == id).first()

        if not payment:
            abort(404)

        data = request.get_json()

        payment.amount = data.get('amount'),
        payment.date = data.get('date'),
        payment.due_date = data.get('due_date'),
        payment.paid = data.get('paid')

        db_session.commit()

        return response('success', 'Successfully updated the item from Payments with Id ' + str(id), 200)
