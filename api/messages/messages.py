from flask import jsonify
from webargs.flaskparser import use_args

from api import db
from api.models import Message, MessageSchema, message_schema
from api.utils import validate_json_content_type, token_required
from api.messages import messages_bp

# @messages_bp.route('/api/v1/messages', methods=['GET'])
# def get_messages():
#     messages = Message.query.all()

#     for message in messages:
#         message.msg_counter += 1
#     db.session.commit()
    
#     return jsonify({
#         'success': True,
#         'data': MessageSchema(many=True).dump(messages),
#         'number_of_records': len(messages)
#     })


@messages_bp.route('/messages/<int:message_id>', methods=['GET'])
def get_message(message_id: int):
    message = Message.query.get_or_404(
        message_id, 
        description=f'Message with id {message_id} not found'
    )
        
    message.msg_counter += 1
    db.session.commit()

    return jsonify({
        'success': True,
        'data': message_schema.dump(message)
    })


@messages_bp.route('/messages', methods=['POST'])
@token_required
@validate_json_content_type
@use_args(message_schema, error_status_code=400)
def create_message(user_id: int, args: dict):
    message = Message(**args)

    db.session.add(message)
    db.session.commit()

    return jsonify({
        'success': True,
        'data': message_schema.dump(message)
    }), 201


@messages_bp.route('/messages/<int:message_id>', methods=['PUT'])
@token_required
@validate_json_content_type
@use_args(message_schema, error_status_code=400)
def update_message(user_id: int, args: dict, message_id: int):
    message = Message.query.get_or_404(
        message_id,
        description=f'Message with id {message_id} not found'
    )
    
    message.msg_text = args['msg_text']
    message.msg_counter = 0
    db.session.commit()

    return jsonify({
        'success': True,
        'data': message_schema.dump(message)
    })


@messages_bp.route('/messages/<int:message_id>', methods=['DELETE'])
@token_required
def delete_message(user_id: int, message_id: int):
    message = Message.query.get_or_404(
        message_id, 
        description=f'Message with id {message_id} not found'
    )    

    db.session.delete(message)
    db.session.commit()

    return jsonify({
        'success': True,
        'data': f'Message with id {message_id} has been deleted'
    })
