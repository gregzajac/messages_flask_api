from flask import Blueprint

messages_bp = Blueprint('messages', __name__)

from api.messages import messages
