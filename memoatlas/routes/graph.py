from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from ..models import db, Tree, Connection

graph = Blueprint('graph', __name__)


@graph.route('/map')
@login_required
def index():
    return render_template('graph/map.html')


@graph.route('/api/graph-data')
@login_required
def graph_data():
    trees = Tree.query.filter_by(user_id=current_user.id).all()
    nodes = []
    for t in trees:
        nodes.append({
            'id': t.id,
            'title': t.title,
            'stage': t.get_stage(),
            'health': t.get_effective_health(),
            'updated_at': (t.updated_at or t.created_at).isoformat()
        })

    links = []
    conns = Connection.query.filter_by(user_id=current_user.id).all()
    for c in conns:
        links.append({
            'source': c.source_id,
            'target': c.target_id
        })

    return jsonify({'nodes': nodes, 'links': links})
