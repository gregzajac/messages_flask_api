import jwt
from flask import current_app
from datetime import datetime, timedelta
from marshmallow import Schema, fields, validate
from api import db


class Message(db.Model):
    
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    msg_text = db.Column(db.String(160), nullable=False)
    msg_counter = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<{self.__class__.__name__}>: {self.id}'


class User(db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True, index=True)
    password = db.Column(db.String(255), nullable=False) 

    def __repr__(self):
        return f'<{self.__class__.__name__}>: {self.username}'

    def generate_jwt(self) -> bytes:
        payload = {
            'user_id': self.id,
            'exp': datetime.utcnow() 
                   + timedelta(minutes=current_app.config.get('JWT_EXPIRED_MINUTES', 30))
        }
        return jwt.encode(payload, current_app.config.get('SECRET_KEY'))


class MessageSchema(Schema):

    id = fields.Integer(dump_only=True)
    msg_text = fields.String(required=True, validate=validate.Length(max=160))
    msg_counter = fields.Integer(dump_only=True)


class UserSchema(Schema):

    id = fields.Integer(dump_only=True)
    username = fields.String(required=True, 
                             validate=validate.Length(min=3, max=255))
    password = fields.String(load_only=True, required=True, 
                             validate=validate.Length(min=6, max=255))


message_schema = MessageSchema()
user_schema = UserSchema()