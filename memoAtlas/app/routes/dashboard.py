from flask import Blueprint, render_template
from flask_login import login_required, current_user
from ..models.note import Note
from ..models.user import db

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/dashboard')
@login_required
def index():
    notes_count = Note.query.filter_by(user_id=current_user.id).count()
    connections_count = 0
    return render_template('dashboard/dashboard.html', notes_count=notes_count, connections_count=connections_count)