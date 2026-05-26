from flask import Blueprint, render_template
from flask_login import login_required, current_user
from ..models.note import Note
from ..models.progress import Progress

game = Blueprint('game', __name__)


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


@game.route('/game')
@login_required
def index():
    user_notes, folders = get_folders(current_user.id)
    progress = Progress.query.filter_by(user_id=current_user.id).first()
    return render_template('game/index.html', notes=user_notes, folders=folders, progress=progress)
