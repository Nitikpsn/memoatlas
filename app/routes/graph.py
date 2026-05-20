from flask import Blueprint

graph = Blueprint('graph', __name__, url_prefix='/graph')

@graph.route('/')
def index():
    return ''