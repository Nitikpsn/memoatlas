from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, abort, request, jsonify
from flask_login import login_required, current_user
from ..models import db, Tree, Connection, Progress

forest = Blueprint('forest', __name__)


def get_or_create_progress(user_id):
    p = Progress.query.filter_by(user_id=user_id).first()
    if not p:
        p = Progress(user_id=user_id, xp=0, level=1)
        db.session.add(p)
        db.session.commit()
    return p


@forest.route('/')
def dashboard():
    if not current_user.is_authenticated:
        return render_template('index.html')
    trees = Tree.query.filter_by(user_id=current_user.id).order_by(Tree.created_at.desc()).all()
    progress = get_or_create_progress(current_user.id)
    total = len(trees)

    stages = {'ancient': [], 'mature': [], 'young': [], 'sprout': [], 'seed': [], 'fading': [], 'wilting': [], 'dead': []}
    total_health = 0
    for t in trees:
        stage = t.get_stage()
        if stage not in stages:
            stage = 'seed'
        stages[stage].append(t)
        total_health += t.get_effective_health()

    forest_health = round(total_health / total, 1) if total > 0 else 0
    needing_care = sum(1 for t in trees if t.needs_care())
    ancient_count = len(stages['ancient'])

    return render_template('forest/dashboard.html',
                           trees=trees, progress=progress, stages=stages,
                           forest_health=forest_health, needing_care=needing_care,
                           total=total, ancient_count=ancient_count)


@forest.route('/plant', methods=['GET', 'POST'])
@login_required
def plant():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        tags = request.form.get('tags', '').strip()

        if not title or not content:
            flash('Title and content are required.', 'danger')
            return redirect(url_for('forest.plant'))

        tree = Tree(title=title, content=content, tags=tags, author=current_user)
        db.session.add(tree)
        db.session.commit()
        flash('Tree planted!', 'success')
        return redirect(url_for('forest.dashboard'))

    return render_template('forest/plant.html')


@forest.route('/tree/<int:tree_id>')
@login_required
def view_tree(tree_id):
    tree = Tree.query.get_or_404(tree_id)
    if tree.author != current_user:
        abort(403)

    connections = Connection.query.filter(
        (Connection.source_id == tree_id) | (Connection.target_id == tree_id),
        Connection.user_id == current_user.id
    ).all()

    connected_trees = []
    for c in connections:
        other_id = c.target_id if c.source_id == tree_id else c.source_id
        other = db.session.get(Tree, other_id)
        if other:
            connected_trees.append(other)

    return render_template('forest/tree.html', tree=tree, connected=connected_trees)


@forest.route('/tree/<int:tree_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_tree(tree_id):
    tree = Tree.query.get_or_404(tree_id)
    if tree.author != current_user:
        abort(403)

    if request.method == 'POST':
        tree.title = request.form.get('title', tree.title)
        tree.content = request.form.get('content', tree.content)
        tree.tags = request.form.get('tags', tree.tags)
        db.session.commit()
        flash('Tree updated.', 'success')
        return redirect(url_for('forest.view_tree', tree_id=tree.id))

    return render_template('forest/edit.html', tree=tree)


@forest.route('/tree/<int:tree_id>/delete', methods=['POST'])
@login_required
def delete_tree(tree_id):
    tree = Tree.query.get_or_404(tree_id)
    if tree.author != current_user:
        abort(403)
    db.session.delete(tree)
    db.session.commit()
    flash('Tree removed from your forest.', 'info')
    return redirect(url_for('forest.dashboard'))


@forest.route('/revise/<int:tree_id>', methods=['GET'])
@login_required
def revise_view(tree_id):
    tree = Tree.query.get_or_404(tree_id)
    if tree.author != current_user:
        abort(403)
    return render_template('forest/revise.html', tree=tree)


@forest.route('/revise/<int:tree_id>', methods=['POST'])
@login_required
def complete_revision(tree_id):
    tree = Tree.query.get_or_404(tree_id)
    if tree.author != current_user:
        return jsonify({'error': 'Unauthorized'}), 403

    tree.last_revised = datetime.utcnow()
    tree.health_score = min(100, tree.health_score + 20)
    db.session.commit()

    return jsonify({
        'success': True,
        'new_health': tree.health_score,
        'stage': tree.get_stage(),
        'message': 'Tree grew stronger!'
    })


@forest.route('/search')
@login_required
def search():
    q = request.args.get('q', '').strip()
    results = []
    if q:
        results = Tree.query.filter(
            Tree.user_id == current_user.id,
            (Tree.title.ilike('%' + q + '%')) | (Tree.content.ilike('%' + q + '%'))
        ).all()
    return render_template('search/results.html', query=q, results=results)


@forest.route('/profile')
@login_required
def profile():
    progress = get_or_create_progress(current_user.id)
    return render_template('forest/profile.html', progress=progress)


@forest.route('/game')
@login_required
def game():
    progress = get_or_create_progress(current_user.id)
    trees = Tree.query.filter_by(user_id=current_user.id).order_by(Tree.created_at.desc()).all()
    return render_template('forest/game.html', progress=progress, trees=trees)
