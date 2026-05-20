from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/notes', methods=['GET'])
@login_required
def get_notes():
    from app.models.note import Note

    subject = request.args.get('subject')
    tag = request.args.get('tag')
    query = request.args.get('q')

    from app.services.search_service import SearchService
    notes = SearchService.search_notes(current_user.id, query, subject, tag)

    return jsonify({
        'notes': [
            {
                'id': note.id,
                'title': note.title,
                'subject': note.subject,
                'tags': note.tag_list,
                'created_at': note.created_at.isoformat(),
                'updated_at': note.updated_at.isoformat(),
            }
            for note in notes
        ]
    })


@api.route('/notes/<int:note_id>', methods=['GET'])
@login_required
def get_note(note_id):
    from app.models.note import Note

    note = Note.query.filter_by(id=note_id, user_id=current_user.id).first()
    if not note:
        return jsonify({'error': 'Note not found'}), 404

    return jsonify({
        'id': note.id,
        'title': note.title,
        'content': note.content,
        'subject': note.subject,
        'tags': note.tag_list,
        'created_at': note.created_at.isoformat(),
        'updated_at': note.updated_at.isoformat(),
    })


@api.route('/graph', methods=['GET'])
@login_required
def get_graph():
    from app.services.graph_service import GraphService

    graph_data = GraphService.get_graph_data(current_user.id)
    return jsonify(graph_data)


@api.route('/graph/connect', methods=['POST'])
@login_required
def create_connection():
    from app.services.graph_service import GraphService
    from app import db

    data = request.get_json()
    source_id = data.get('source_id')
    target_id = data.get('target_id')
    description = data.get('description')
    strength = data.get('strength', 1.0)

    if not source_id or not target_id:
        return jsonify({'error': 'source_id and target_id are required'}), 400

    connection = GraphService.create_connection(
        current_user.id, source_id, target_id, description, strength
    )
    if not connection:
        return jsonify({'error': 'Could not create connection'}), 400

    return jsonify({
        'id': connection.id,
        'source': connection.source_note_id,
        'target': connection.target_note_id,
        'description': connection.description,
        'strength': connection.strength,
    }), 201


@api.route('/graph/connect/<int:connection_id>', methods=['DELETE'])
@login_required
def delete_connection(connection_id):
    from app.services.graph_service import GraphService

    if GraphService.remove_connection(current_user.id, connection_id):
        return jsonify({'message': 'Connection removed'}), 200
    return jsonify({'error': 'Connection not found'}), 404


@api.route('/search', methods=['GET'])
@login_required
def search():
    from app.services.search_service import SearchService

    query = request.args.get('q', '')
    subject = request.args.get('subject')
    tag = request.args.get('tag')

    notes = SearchService.search_notes(current_user.id, query, subject, tag)
    return jsonify({
        'notes': [
            {
                'id': note.id,
                'title': note.title,
                'subject': note.subject,
                'tags': note.tag_list,
            }
            for note in notes
        ]
    })


@api.route('/stats', methods=['GET'])
@login_required
def stats():
    from app.services.analytics_service import AnalyticsService

    stats = AnalyticsService.get_user_stats(current_user)
    return jsonify(stats)
