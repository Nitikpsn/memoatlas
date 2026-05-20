from flask import Blueprint, render_template
from flask_login import login_required, current_user

dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard.route('/')
@login_required
def index():
    from app.services.analytics_service import AnalyticsService
    from app.models.note import Note

    stats = AnalyticsService.get_user_stats(current_user)
    recent_notes = Note.query.filter_by(user_id=current_user.id).order_by(Note.updated_at.desc()).limit(5).all()
    recent_activity = AnalyticsService.get_recent_activity(current_user, limit=10)

    return render_template(
        'dashboard/dashboard.html',
        stats=stats,
        recent_notes=recent_notes,
        recent_activity=recent_activity
    )
