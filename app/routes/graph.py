from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user

graph_bp = Blueprint('graph', __name__, url_prefix='/graph')


@graph_bp.route('/')
@login_required
def index():
    from app.services.graph_service import GraphService

    graph_data = GraphService.get_graph_data(current_user.id)
    return render_template('graph/graph.html', graph_data=graph_data)


@graph_bp.route('/data')
@login_required
def data():
    from app.services.graph_service import GraphService

    graph_data = GraphService.get_graph_data(current_user.id)
    return jsonify(graph_data)
