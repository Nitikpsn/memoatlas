from flask import Blueprint, render_template
from flask_login import login_required, current_user

notes = Blueprint('notes', __name__, url_prefix='/notes')


@notes.route('/')
@login_required
def index():
    from app.models.note import Note
    notes_list = Note.query.filter_by(user_id=current_user.id).order_by(Note.updated_at.desc()).all()
    return render_template('notes/list.html', notes=notes_list)


@notes.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    from flask import redirect, url_for, flash
    from app.forms.note_form import NoteForm
    from app.models.note import Note
    from app.services.analytics_service import AnalyticsService
    from app import db

    form = NoteForm()
    if form.validate_on_submit():
        note = Note(
            title=form.title.data,
            content=form.content.data,
            subject=form.subject.data,
            tags=form.tags.data,
            user_id=current_user.id
        )
        db.session.add(note)
        db.session.commit()
        AnalyticsService.log_progress(current_user.id, 'note_created', note.id)
        flash('Note created!', 'success')
        return redirect(url_for('notes.detail', note_id=note.id))
    return render_template('notes/create.html', form=form)


@notes.route('/<int:note_id>')
@login_required
def detail(note_id):
    from flask import abort
    from app.models.note import Note
    from app.services.graph_service import GraphService

    note = Note.query.filter_by(id=note_id, user_id=current_user.id).first_or_404()
    connected_notes = GraphService.get_connected_notes(note_id, current_user.id)
    return render_template('notes/detail.html', note=note, connected_notes=connected_notes)


@notes.route('/<int:note_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(note_id):
    from flask import redirect, url_for, flash, abort
    from app.forms.note_form import NoteForm
    from app.models.note import Note
    from app.services.analytics_service import AnalyticsService
    from app import db

    note = Note.query.filter_by(id=note_id, user_id=current_user.id).first_or_404()
    form = NoteForm(obj=note)

    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data
        note.subject = form.subject.data
        note.tags = form.tags.data
        db.session.commit()
        AnalyticsService.log_progress(current_user.id, 'note_updated', note.id)
        flash('Note updated!', 'success')
        return redirect(url_for('notes.detail', note_id=note.id))
    return render_template('notes/edit.html', form=form, note=note)


@notes.route('/<int:note_id>/delete', methods=['POST'])
@login_required
def delete(note_id):
    from flask import redirect, url_for, flash, abort
    from app.models.note import Note
    from app.models.connection import Connection
    from app.services.analytics_service import AnalyticsService
    from app import db

    note = Note.query.filter_by(id=note_id, user_id=current_user.id).first_or_404()
    Connection.query.filter(
        (Connection.user_id == current_user.id) &
        ((Connection.source_note_id == note_id) | (Connection.target_note_id == note_id))
    ).delete()
    db.session.delete(note)
    db.session.commit()
    AnalyticsService.log_progress(current_user.id, 'note_deleted', note_id)
    flash('Note deleted.', 'info')
    return redirect(url_for('notes.index'))
