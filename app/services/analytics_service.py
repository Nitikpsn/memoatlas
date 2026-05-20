from app import db
from app.models.note import Note
from app.models.connection import Connection
from app.models.progress import Progress
from datetime import datetime, timezone, timedelta


class AnalyticsService:

    @staticmethod
    def get_user_stats(user):
        note_count = Note.query.filter_by(user_id=user.id).count()
        connection_count = Connection.query.filter_by(user_id=user.id).count()
        subject_counts = (
            db.session.query(Note.subject, db.func.count(Note.id))
            .filter_by(user_id=user.id)
            .group_by(Note.subject)
            .all()
        )
        return {
            'note_count': note_count,
            'connection_count': connection_count,
            'subject_distribution': dict(subject_counts),
        }

    @staticmethod
    def get_recent_activity(user, limit=10):
        return (
            Progress.query
            .filter_by(user_id=user.id)
            .order_by(Progress.timestamp.desc())
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_note_activity(user, days=30):
        cutoff = datetime.utcnow() - timedelta(days=days)
        return (
            Note.query
            .filter(Note.user_id == user.id, Note.created_at >= cutoff)
            .order_by(Note.created_at.desc())
            .all()
        )

    @staticmethod
    def log_progress(user_id, action, note_id=None, details=None):
        entry = Progress(
            user_id=user_id,
            note_id=note_id,
            action=action,
            details=details
        )
        from app import db
        db.session.add(entry)
        db.session.commit()
        return entry
