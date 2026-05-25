from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models.note import Note

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