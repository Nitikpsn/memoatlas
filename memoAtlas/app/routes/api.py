from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from ..models.note import Note
from ..models.connection import Connection
from ..models.progress import Progress
from ..models import db
from ..services.graph_service import create_connection

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/')
def index():
    return ''


def jaccard_similarity(tags_a, tags_b):
    """calculate how similar two tag lists are (0.0 to 1.0)"""
    set_a = set(tags_a)
    set_b = set(tags_b)

    # if both are empty, they are not similar
    if not set_a and not set_b:
        return 0.0

    # find tags in common
    intersection = set_a & set_b
    union = set_a | set_b

    return len(intersection) / len(union)


@api.route('/gravity/<int:note_id>')
@login_required
def gravity(note_id):
    """find notes similar to a given note by tag matching"""
    note = Note.query.get_or_404(note_id)
    if note.author != current_user:
        return jsonify({'error': 'forbidden'}), 403

    target_tags = note.get_tag_list()
    user_notes = Note.query.filter(
        Note.user_id == current_user.id,
        Note.id != note_id
    ).all()

    # score each note by how similar its tags are
    scored = []
    for other in user_notes:
        score = jaccard_similarity(target_tags, other.get_tag_list())
        scored.append({
            'id': str(other.id),
            'title': other.title,
            'proximityScore': round(score, 4),
            'tags': other.get_tag_list()
        })

    # sort by similarity (highest first) and return top 3
    scored.sort(key=lambda x: x['proximityScore'], reverse=True)
    return jsonify(scored[:3])


@api.route('/gravity-by-content')
@login_required
def gravity_by_content():
    """find notes similar to a search query"""
    q = request.args.get('q', '').strip()
    if not q:
        return jsonify([])

    query_words = set(q.lower().split())
    user_notes = Note.query.filter(Note.user_id == current_user.id).all()

    scored = []
    for other in user_notes:
        # combine title, content, and tags into one bag of words
        content_words = set((other.title + ' ' + other.content).lower().split())
        tag_words = set(other.get_tag_list())
        all_words = content_words | tag_words

        if not all_words:
            continue

        # check how many search words match
        intersection = query_words & all_words
        union = query_words | all_words
        score = len(intersection) / len(union)

        if score > 0:
            scored.append({
                'id': str(other.id),
                'title': other.title,
                'proximityScore': round(score, 4),
                'tags': other.get_tag_list()
            })

    scored.sort(key=lambda x: x['proximityScore'], reverse=True)
    return jsonify(scored[:3])


@api.route('/link', methods=['POST'])
@login_required
def create_link():
    """connect two notes together"""
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

    # check if either note was unmatched before this link
    was_unmatched = not source_note.is_matched or not target_note.is_matched

    # create the connection
    conn = create_connection(
        current_user.id, source_id, target_id,
        relationship_type=data.get('type', 'related')
    )

    # update xp
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
