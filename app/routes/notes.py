from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.user import db
from app.models.note import Note
from app.forms.note_form import NoteForm

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
        return redirect(url_for('dashboard.index'))
    return render_template('notes/create_note.html', form=form)