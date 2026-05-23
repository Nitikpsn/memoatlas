from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from ..services.search_service import search_notes

search_bp = Blueprint('search', __name__)

@search_bp.route('/search')
@login_required
def index():
    q = request.args.get('q', '').strip()
    results = search_notes(current_user.id, q) if q else []
    return render_template('search/results.html', query=q, results=results)

@search_bp.route('/api/search')
@login_required
def api_search():
    q = request.args.get('q', '').strip()
    results = search_notes(current_user.id, q) if q else []
    return jsonify([{
        'id': n.id,
        'title': n.title,
        'snippet': n.content[:150]
    } for n in results])
