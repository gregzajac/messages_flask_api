import json
from pathlib import Path

from api import db
from api.models import Message
from api.commands import db_manage_bp


@db_manage_bp.cli.group()
def db_manage():
    """Database management commands"""
    pass


@db_manage.command()
def add_data():
    """Add sample data to the database"""
    
    try:
        messages_path = Path(__file__).parent.parent / 'samples' / 'messages.json'

        with open(messages_path) as file:
            data_json = json.load(file)
        
        for item in data_json:
            message = Message(**item)
            db.session.add(message)
        
        db.session.commit()
        print('Data has been succesfully added to the database')

    except Exception as exc:
        print(f'Unexpected error: {exc}')


@db_manage.command()
def remove_data():
    """Remove all data from the database"""
    
    try:
        db.session.execute('DELETE FROM messages')
        db.session.execute('ALTER SEQUENCE messages_id_seq RESTART WITH 1;')
        db.session.commit()
        print('All data has been deleted from the database')

    except Exception as exc:
        print(f'Unexpected error: {exc}')
