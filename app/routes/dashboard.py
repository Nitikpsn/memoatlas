from flask import Blueprint, render_template
from flask_login import login_required, current_user

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/dashboard')
@login_required
def index():
    notes_count = 0
    connections_count = 0
    return render_template('dashboard/dashboard.html',
                         user=current_user,
                         notes_count=notes_count,
                         connections_count=connections_count)