from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_required, current_user
from app import db
from app.models.note import Note
from app.forms.note_form import NoteForm

notes = Blueprint('notes', __name__)

@notes.route("/note/new", methods=['GET', 'POST'])
@login_required
def create_note():
    form = NoteForm()
    if form.validate_on_submit():
        note = Note(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(note)
        db.session.commit()
        flash('Node created in your Atlas!', 'success')
        return redirect(url_for('dashboard.index'))
    return render_template('notes/create_note.html', title='New Note', form=form)

@notes.route("/notes")
@login_required
def index():
    # Fetching all notes for the current user
    user_notes = Note.query.filter_by(user_id=current_user.id).order_by(Note.date_posted.desc()).all()
    return render_template('notes/list_notes.html', notes=user_notes)