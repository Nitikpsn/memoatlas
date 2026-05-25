from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models.note import Note
from app.models.connection import Connection
from app.models.progress import Progress
from app.models.user import db
from app.services.graph_service import GraphService

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/')
def index():
    return ''

def _jaccard_similarity(a_tags, b_tags):
    set_a = set(a_tags)
    set_b = set(b_tags)
    if not set_a and not set_b:
        return 0.0
    intersection = set_a & set_b
    union = set_a | set_b
    return len(intersection) / len(union)

@api.route('/gravity/<int:note_id>')
@login_required
def gravity(note_id):
    note = Note.query.get_or_404(note_id)
    if note.author != current_user:
        return jsonify({'error': 'forbidden'}), 403

    target_tags = note.tag_list()
    user_notes = Note.query.filter(
        Note.user_id == current_user.id,
        Note.id != note_id
    ).all()

    scored = []
    for other in user_notes:
        score = _jaccard_similarity(target_tags, other.tag_list())
        scored.append({
            'id': str(other.id),
            'title': other.title,
            'proximityScore': round(score, 4),
            'tags': other.tag_list()
        })

    scored.sort(key=lambda x: x['proximityScore'], reverse=True)
    return jsonify(scored[:3])

@api.route('/gravity-by-content')
@login_required
def gravity_by_content():
    q = request.args.get('q', '').strip()
    if not q:
        return jsonify([])

    query_words = set(q.lower().split())
    user_notes = Note.query.filter(Note.user_id == current_user.id).all()

    scored = []
    for other in user_notes:
        content_words = set((other.title + ' ' + other.content).lower().split())
        tag_words = set(other.tag_list())
        all_words = content_words | tag_words
        if not all_words:
            continue
        intersection = query_words & all_words
        union = query_words | all_words
        score = len(intersection) / len(union)
        if score > 0:
            scored.append({
                'id': str(other.id),
                'title': other.title,
                'proximityScore': round(score, 4),
                'tags': other.tag_list()
            })

    scored.sort(key=lambda x: x['proximityScore'], reverse=True)
    return jsonify(scored[:3])

@api.route('/link', methods=['POST'])
@login_required
def create_link():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    source_id = data.get('source_id')
    target_id = data.get('target_id')
    if not source_id or not target_id:
        return jsonify({'error': 'source_id and target_id required'}), 400

    source_note = db.session.get(Note, source_id)
    target_note = db.session.get(Note, target_id)
    if not source_note or not target_note:
        return jsonify({'error': 'Note not found'}), 404
    if source_note.author != current_user or target_note.author != current_user:
        return jsonify({'error': 'Forbidden'}), 403

    was_unmatched = not source_note.is_matched or not target_note.is_matched

    conn = GraphService.create_connection(
        current_user.id, source_id, target_id,
        relationship_type=data.get('type', 'related')
    )

    progress = Progress.query.filter_by(user_id=current_user.id).first()
    if not progress:
        progress = Progress(user_id=current_user.id, xp=0, level=1)
        db.session.add(progress)

    xp_gained = 0
    if was_unmatched:
        xp_gained = 100
        progress.xp += xp_gained
        db.session.commit()

    return jsonify({
        'connection': {
            'id': conn.id,
            'source_id': conn.source_note_id,
            'target_id': conn.target_note_id,
        },
        'xp_gained': xp_gained,
        'total_xp': progress.xp,
        'source_matched': source_note.is_matched,
        'target_matched': target_note.is_matched,
    })