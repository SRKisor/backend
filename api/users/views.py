from flask import jsonify, request, Blueprint,current_app
from flask_security import current_user
from flask_security.utils import login_user, verify_password,hash_password,logout_user

from api.database import db_session

from api import security

from api.helpers import response, require_login,required_roles

from api.users.models import User

from api.users.Schema import user_schema,users_schema


users_bp = Blueprint('auth', __name__, url_prefix='/auth')


@users_bp.route('/register', methods=('GET', 'POST'))
@require_login
@required_roles('admin')
def register():
    if not request.content_type == 'application/json':
        return response('Failed', 'Content-type must be application/json', 401)

    data = request.get_json()

    fields = ['email', 'username', 'password']
    string = ''

    for i in fields:
        if not data.get(f'{i}'):
            string = string+f'\"{i}\", '

    if string:
        return response('Invalid POST Request', f'These fields should be included in the POST Request. {string}', 404)

    user = User.query.filter(User.email == data.get('username')).first()

    if user:
        return response('Not Found', f'User with username {user} alreay exists.', 404)

    security.datastore.create_user(email=data.get('email'), username=data.get(
        'username'), password=hash_password(data.get('password')))

    security.datastore.commit()

    return 'success'


@users_bp.route('/login', methods=('GET', 'POST'))
def login():
    if not request.content_type == 'application/json':
        return response('Failed', 'Content-type must be application/json', 401)

    data = request.get_json()

    fields = ['username', 'password']
    string = ''

    for i in fields:
        if not data.get(f'{i}'):
            string = string+f'\"{i}\", '

    if string:
        return response('Invalid POST Request', f'These fields should be included in the POST Request. {string}', 404)

    user = User.query.filter(User.email == data.get('username')).first()

    if not user:
        return response('Not Found', f'User with username {user} does not exists.', 404)

    if not verify_password(data.get('password'), user.password):
        return response('Wrong Password', f'Password for user {user.username} does not match.', 404)

    login_user(user, remember=True)

    security.datastore.commit()

    return response('Success', f'User {user.username} Successfully Logged In.', 200, user_schema.dump(user), user.get_auth_token())


@users_bp.route('/logout')
@require_login
def logout():
    logout_user()

    return 'logout'


@users_bp.route('/')
# @require_login
def get_all_users():
    users = User.query.all()

    return response('User List', 'Full user list', 200, users_schema.dump(users), current_user.get_auth_token())
