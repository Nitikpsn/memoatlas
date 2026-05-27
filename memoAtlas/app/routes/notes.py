from flask import Blueprint, render_template, redirect, url_for, flash, abort, request, jsonify
from flask_login import login_required, current_user
from ..models import db
from ..models.note import Note
from ..forms.note_form import NoteForm
from datetime import datetime

notes = Blueprint('notes', __name__)


def get_folders(user_id):
    """organize notes by month/year for the sidebar"""
    user_notes = Note.query.filter_by(user_id=user_id).order_by(Note.date_posted.desc()).all()
    folders = {}
    for note in user_notes:
        month_key = note.date_posted.strftime('%B %Y')
        if month_key not in folders:
            folders[month_key] = []
        folders[month_key].append(note)
    return user_notes, folders


@notes.route('/workspace')
@login_required
def workspace():
    user_notes, folders = get_folders(current_user.id)
    return render_template('notes/list_notes.html', notes=user_notes, folders=folders)


@notes.route('/notes')
@login_required
def index():
    return redirect(url_for('notes.workspace'))


@notes.route('/note/new', methods=['GET', 'POST'])
@login_required
def create_note():
    form = NoteForm()
    user_notes, folders = get_folders(current_user.id)

    if form.validate_on_submit():
        new_note = Note(
            title=form.title.data,
            content=form.content.data,
            tags=form.tags.data,
            author=current_user
        )
        db.session.add(new_note)
        db.session.commit()
        flash('Note added to your Atlas!', 'success')
        return redirect(url_for('notes.workspace'))

    return render_template('notes/create_note.html', form=form, notes=user_notes, folders=folders)


@notes.route('/note/<int:note_id>')
@login_required
def view_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.author != current_user:
        abort(403)
    return render_template('notes/detail.html', note=note)


@notes.route('/note/<int:note_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.author != current_user:
        abort(403)

    user_notes, folders = get_folders(current_user.id)
    form = NoteForm(obj=note)

    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data
        note.tags = form.tags.data
        db.session.commit()
        flash('Note updated!', 'success')
        return redirect(url_for('notes.view_note', note_id=note.id))

    return render_template('notes/edit.html', form=form, note=note, notes=user_notes, folders=folders)


@notes.route('/note/<int:note_id>/delete', methods=['POST'])
@login_required
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.author != current_user:
        abort(403)
    db.session.delete(note)
    db.session.commit()
    flash('Note deleted.', 'info')
    return redirect(url_for('notes.workspace'))


@notes.route('/revise/<int:note_id>', methods=['POST'])
@login_required
def complete_revision(note_id):
    note = Note.query.get_or_404(note_id)
    if note.author != current_user:
        return jsonify({"error": "Unauthorized"}), 403
    note.last_revised = datetime.utcnow()
    note.health_score += 20
    if note.health_score > 100:
        note.health_score = 100
    db.session.commit()
    return jsonify({
        "success": True,
        "new_health": note.health_score,
        "message": "Tree grew successfully!"
    })


@notes.route('/revise/<int:note_id>', methods=['GET'])
@login_required
def revise_view(note_id):
    note = Note.query.get_or_404(note_id)
    if note.author != current_user:
        abort(403)
    return render_template('dashboard/revise.html', note=note)
