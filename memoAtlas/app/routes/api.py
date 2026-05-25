from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models.note import Note

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/')
def index():
    return ''

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
        other_tags = other.tag_list()
        shared = len(set(target_tags) & set(other_tags))
        if shared > 0 or not target_tags:
            scored.append({
                'id': str(other.id),
                'title': other.title,
                'proximityScore': shared,
                'tags': other_tags
            })

    scored.sort(key=lambda x: x['proximityScore'], reverse=True)
    return jsonify(scored[:3])

@api.route('/gravity-by-content')
@login_required
def gravity_by_content():
    q = request.args.get('q', '').strip()
    if not q:
        return jsonify([])

    words = q.lower().split()
    user_notes = Note.query.filter(Note.user_id == current_user.id).all()

    scored = []
    for other in user_notes:
        content = (other.title + ' ' + other.content).lower()
        word_matches = sum(1 for w in words if w in content)
        tag_matches = len(set(words) & set(other.tag_list()))
        score = word_matches + (tag_matches * 3)
        if score > 0:
            scored.append({
                'id': str(other.id),
                'title': other.title,
                'proximityScore': score,
                'tags': other.tag_list()
            })

    scored.sort(key=lambda x: x['proximityScore'], reverse=True)
    return jsonify(scored[:3])