from app import db
from datetime import datetime, timezone


class Progress(db.Model):
    __tablename__ = 'progress'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    note_id = db.Column(db.Integer, db.ForeignKey('notes.id'), nullable=True, index=True)
    action = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    details = db.Column(db.Text, nullable=True)

    note = db.relationship('Note', backref='progress_entries')

    def __repr__(self):
        return f'<Progress {self.action} by user {self.user_id}>'
