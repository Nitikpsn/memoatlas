from flask import Blueprint

notes = Blueprint('notes', __name__, url_prefix='/notes')

@notes.route('/')
def index():
    return ''