from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from ..services.graph_service import get_graph_data

graph = Blueprint('graph', __name__)


@graph.route('/graph')
@login_required
def index():
    return render_template('graph/index.html')


@graph.route('/api/graph-data')
@login_required
def graph_data():
    data = get_graph_data(current_user.id)
    return jsonify(data)
