from flask import Blueprint, render_template, redirect, url_for, flash, abort, request
from flask_login import login_required, current_user
from app.models.user import db
from app.models.note import Note
from app.forms.note_form import NoteForm
from datetime import datetime

notes = Blueprint('notes', __name__)

@notes.route('/notes')
@login_required
def index():
    user_notes = Note.query.filter_by(user_id=current_user.id).all()
    return render_template('notes/list_notes.html', notes=user_notes)

@notes.route('/note/new', methods=['GET', 'POST'])
@login_required
def create_note():
    form = NoteForm()
    if form.validate_on_submit():
        new_note = Note(
            title=form.title.data,
            content=form.content.data,
            author=current_user
        )
        db.session.add(new_note)
        db.session.commit()
        flash('Note added to your Atlas!', 'success')
        return redirect(url_for('notes.index'))
    return render_template('notes/create_note.html', form=form)

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
    form = NoteForm(obj=note)
    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data
        note.date_posted = datetime.utcnow()
        db.session.commit()
        flash('Note updated!', 'success')
        return redirect(url_for('notes.view_note', note_id=note.id))
    return render_template('notes/edit.html', form=form, note=note)

@notes.route('/note/<int:note_id>/delete', methods=['POST'])
@login_required
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.author != current_user:
        abort(403)
    db.session.delete(note)
    db.session.commit()
    flash('Note deleted.', 'info')
    return redirect(url_for('notes.index'))