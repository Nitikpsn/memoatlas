from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models.note import Note
from collections import defaultdict

game = Blueprint('game', __name__)

@game.route('/game')
@login_required
def index():
    user_notes = Note.query.filter_by(user_id=current_user.id).order_by(Note.date_posted.desc()).all()
    folders = defaultdict(list)
    for note in user_notes:
        month_key = note.date_posted.strftime('%B %Y')
        folders[month_key].append(note)
    return render_template('game/index.html', notes=user_notes, folders=dict(folders))
