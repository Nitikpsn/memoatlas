from flask import Blueprint, render_template, redirect, url_for, flash, abort, request
from flask_login import login_required, current_user
from app.models.user import db
from app.models.note import Note
from app.forms.note_form import NoteForm
from datetime import datetime
from collections import defaultdict

notes = Blueprint('notes', __name__)

@notes.route('/workspace')
@login_required
def workspace():
    user_notes = Note.query.filter_by(user_id=current_user.id).order_by(Note.date_posted.desc()).all()

    folders = defaultdict(list)
    for note in user_notes:
        month_key = note.date_posted.strftime('%B %Y')
        folders[month_key].append(note)

    return render_template('notes/list_notes.html', notes=user_notes, folders=dict(folders))

@notes.route('/notes')
@login_required
def index():
    return redirect(url_for('notes.workspace'))

@notes.route('/note/new', methods=['GET', 'POST'])
@login_required
def create_note():
    form = NoteForm()
    user_notes = Note.query.filter_by(user_id=current_user.id).order_by(Note.date_posted.desc()).all()
    folders = defaultdict(list)
    for note in user_notes:
        month_key = note.date_posted.strftime('%B %Y')
        folders[month_key].append(note)

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
    return render_template('notes/create_note.html', form=form, notes=user_notes, folders=dict(folders))

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
    user_notes = Note.query.filter_by(user_id=current_user.id).order_by(Note.date_posted.desc()).all()
    folders = defaultdict(list)
    for n in user_notes:
        month_key = n.date_posted.strftime('%B %Y')
        folders[month_key].append(n)

    form = NoteForm(obj=note)
    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data
        note.tags = form.tags.data
        note.date_posted = datetime.utcnow()
        db.session.commit()
        flash('Note updated!', 'success')
        return redirect(url_for('notes.view_note', note_id=note.id))
    return render_template('notes/edit.html', form=form, note=note, notes=user_notes, folders=dict(folders))

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