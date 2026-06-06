from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from ..models import db, Tree, Connection, Progress

api = Blueprint('api', __name__, url_prefix='/api')


def jaccard(a, b):
    set_a = set(a)
    set_b = set(b)
    if not set_a and not set_b:
        return 0.0
    union = set_a | set_b
    return len(set_a & set_b) / len(union)


@api.route('/gravity/<int:tree_id>')
@login_required
def gravity(tree_id):
    tree = Tree.query.get_or_404(tree_id)
    if tree.author != current_user:
        return jsonify({'error': 'forbidden'}), 403

    target_tags = tree.get_tag_list()
    others = Tree.query.filter(
        Tree.user_id == current_user.id,
        Tree.id != tree_id
    ).all()

    scored = []
    for o in others:
        score = jaccard(target_tags, o.get_tag_list())
        scored.append({
            'id': o.id,
            'title': o.title,
            'score': round(score, 4),
            'tags': o.get_tag_list()
        })

    scored.sort(key=lambda x: x['score'], reverse=True)
    return jsonify(scored[:3])


@api.route('/gravity-by-content')
@login_required
def gravity_by_content():
    q = request.args.get('q', '').strip()
    if not q:
        return jsonify([])

    words = set(q.lower().split())
    others = Tree.query.filter(Tree.user_id == current_user.id).all()

    scored = []
    for o in others:
        text = set((o.title + ' ' + o.content).lower().split())
        tags = set(o.get_tag_list())
        all_words = text | tags
        if not all_words:
            continue
        score = len(words & all_words) / len(words | all_words)
        if score > 0:
            scored.append({
                'id': o.id,
                'title': o.title,
                'score': round(score, 4),
                'tags': o.get_tag_list()
            })

    scored.sort(key=lambda x: x['score'], reverse=True)
    return jsonify(scored[:3])


@api.route('/link', methods=['POST'])
@login_required
def create_link():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data'}), 400

    source = data.get('source_id')
    target = data.get('target_id')
    if not source or not target:
        return jsonify({'error': 'source_id and target_id required'}), 400

    s = db.session.get(Tree, source)
    t = db.session.get(Tree, target)
    if not s or not t:
        return jsonify({'error': 'Tree not found'}), 404
    if s.author != current_user or t.author != current_user:
        return jsonify({'error': 'Forbidden'}), 403

    existing = Connection.query.filter(
        ((Connection.source_id == source) & (Connection.target_id == target)) |
        ((Connection.source_id == target) & (Connection.target_id == source))
    ).first()
    if existing:
        return jsonify({'error': 'Already connected'}), 400

    conn = Connection(source_id=source, target_id=target, user_id=current_user.id)
    db.session.add(conn)

    progress = Progress.query.filter_by(user_id=current_user.id).first()
    if not progress:
        progress = Progress(user_id=current_user.id, xp=0, level=1)
        db.session.add(progress)

    progress.xp += 100
    db.session.commit()

    return jsonify({
        'connection': {'id': conn.id, 'source': conn.source_id, 'target': conn.target_id},
        'xp_gained': 100,
        'total_xp': progress.xp,
        'level': progress.level
    })
