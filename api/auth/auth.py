from flask import jsonify, abort
from webargs.flaskparser import use_args
from werkzeug.security import generate_password_hash, check_password_hash

from api import db
from api.auth import auth_bp
from api.utils import validate_json_content_type, token_required
from api.models import User, UserSchema, user_schema


@auth_bp.route('/register', methods=['POST'])
@validate_json_content_type
@use_args(user_schema, error_status_code=400)
def register(args: dict):
    if User.query.filter(User.username == args['username']).first():
        abort(409, description=f'User with username {args["username"]} already exists')

    args['password'] = generate_password_hash(args['password'])
    user = User(**args)

    db.session.add(user)
    db.session.commit()

    token = user.generate_jwt()
    
    return jsonify({
        'success': True,
        'token': token.decode()
    }), 201


@auth_bp.route('/login', methods=['POST'])
@validate_json_content_type
@use_args(user_schema, error_status_code=400)
def login(args: dict):
    user = User.query.filter(User.username == args['username']).first()
    
    if not user:
        abort(401, description=f'Invalid credentials')

    if not check_password_hash(user.password, args['password']):    
        abort(401, description=f'Invalid credentials')

    token = user.generate_jwt()

    return jsonify({
        'success': True,
        'token': token.decode()
    })


@auth_bp.route('/me', methods=['GET'])
@token_required
def get_current_user(user_id: int):
    user = User.query.get_or_404(
        int(user_id),
        description=f'User with id {user_id} not found' 
    )

    return jsonify({
        'success': True,
        'data': user_schema.dump(user)
    })
