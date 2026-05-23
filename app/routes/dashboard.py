@dashboard.route('/dashboard')
@login_required
def index():
    # This actually counts your real notes in the DB
    note_count = Note.query.filter_by(user_id=current_user.id).count()
    return render_template('dashboard/dashboard.html', note_count=note_count)