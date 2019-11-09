import os

import click
from flask import Flask, request, jsonify,current_app
from flask.cli import with_appcontext
from flask_marshmallow import Marshmallow
from api.database import Base, db_session
from flask_migrate import Migrate
from flask_cors import CORS
from flask_security import Security, SQLAlchemySessionUserDatastore, current_user
from werkzeug.middleware.proxy_fix import ProxyFix

from api.config import DATA_SOURCE

ma = Marshmallow()

security = Security()

def create_app(test_config=None):
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY='c5282ad3ea38420ab8ac0326a48d3a8c',
        SQLALCHEMY_DATABASE_URI=DATA_SOURCE,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SECURITY_TRACKABLE=True,
        SECURITY_PASSWORD_SALT='bf9797d59d094abb92fdca167494a7ee',
        SECURITY_UNAUTHORIZED_VIEW='/login',
        SECURITY_REGISTERABLE=False
    )

    CORS(app)

    ma.init_app(app)

    migrate = Migrate(app, Base)

    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1)

    from api.users.models import User, Role

    user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)

    security.init_app(app, datastore=user_datastore,register_blueprint=False)

    # @app.before_request
    # def before_request_func():
    #     if not current_user.is_authenticated:
    #         return 'not loged in'

    def register_api(view, endpoint, url, pk='id', pk_type='int'):
        view_func = view.as_view(endpoint)
        app.add_url_rule(url, defaults={pk: None},
                         view_func=view_func, methods=['GET', ])
        app.add_url_rule(url, view_func=view_func, methods=['POST', ])
        app.add_url_rule('%s<%s:%s>' % (url, pk_type, pk), view_func=view_func,
                         methods=['GET', 'PUT', 'DELETE'])

    from api.items import ItemsAPI
    from api.distributors import DistributorsAPI
    from api.clients import ClientsAPI
    from api.payments import PaymentsAPI
    from api.bill import BillsAPI

    register_api(ItemsAPI, 'items_api', '/items/', pk='item_code')
    register_api(DistributorsAPI, 'distributor_api',
                 '/distributors/', pk='id')
    register_api(ClientsAPI, 'clients_api', '/clients/', pk='id')
    register_api(PaymentsAPI, 'payments_api', '/payments/', pk='id')
    register_api(BillsAPI, 'bills_api', '/bills/', pk='id')

    from api.users import users_bp

    app.register_blueprint(users_bp, url_prefix='/users')

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        from api.database import db_session
        db_session.remove()

    return app
