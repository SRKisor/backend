from flask import make_response, jsonify
from flask_security import current_user
from functools import wraps
from api import security

from api.users.models import User


def response(status, message, status_code, data=[], token=""):
    """
    Make an http response helper
    :param status: Status message
    :param message: Response Message
    :param status_code: Http response code
    :return:
    """
    if data:
        return make_response(jsonify({
            'status': status,
            'message': message,
            'data': data,
            'token': token,
            'status code': str(status_code)
        })), status_code

    return make_response(jsonify({
        'status': status,
        'message': message,
        'status code': str(status_code)
    })), status_code


def require_login(f):
    @wraps(f)
    def require_login_function(*args, **kwargs):
        if current_user.is_authenticated:
            return f(*args, **kwargs)
        else:
            return response('Forbidden Request', f'This user does not have access to this endpoint', 403)
    return require_login_function


def required_roles(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            for i in roles:
                if not current_user.has_role(i):
                    return response('Forbidden Request', f'This user does not have the access level to access this endpoint', 403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# def require_api_key(api_method):
#     @wraps(api_method)
#     def check_api_key(*args, **kwargs):
#         apikey = request.headers.get('ApiKey')
#         if apikey and apikey == SECRET_KEY:
#             return api_method(*args, **kwargs)
#         else:
#             abort(401)

#     return check_api_key
