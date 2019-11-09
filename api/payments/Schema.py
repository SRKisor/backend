from api import ma
from api.payments.models import Payment_Methods, Payment_Types, Payments


class Payment_TypesSchema(ma.ModelSchema):
    class Meta:
        model = Payment_Types


class Payment_MethodsSchema(ma.ModelSchema):
    class Meta:
        model = Payment_Methods


class PaymentsSchema(ma.ModelSchema):
    class Meta:
        model = Payments

    payment_methods_name = ma.Function(
        lambda obj: obj.payment_types.type_name)
    payment_types_name = ma.Function(
        lambda obj: obj.payment_methods.method_name)


payment_schema = PaymentsSchema(many=False)
payments_schema = PaymentsSchema(many=True)
