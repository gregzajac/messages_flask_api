import jwt
from flask import request, abort, current_app
from werkzeug.exceptions import UnsupportedMediaType
from functools import wraps


def validate_json_content_type(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        data = request.get_json()
        if data is None:
            raise UnsupportedMediaType('Content type must be application/json')
        return func(*args, **kwargs)
    return wrapper


def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = None
        auth = request.headers.get('Authorization')

        if auth:
            token = auth.split(' ')[1]
        if token is None:
            abort(401, description='Missing token, please login or register')
        
        try:
            payload = jwt.decode(token, 
                                 current_app.config.get('SECRET_KEY'), 
                                 algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            abort(401, description='Expired token, please login to get new token')
        except jwt.InvalidTokenError:
            abort(401, description='Invalid token, please login or register')
        else:
            return func(payload['user_id'], *args, **kwargs)
    return wrapper
