from app import db
from datetime import datetime, timezone


class Connection(db.Model):
    __tablename__ = 'connections'

    id = db.Column(db.Integer, primary_key=True)
    source_note_id = db.Column(db.Integer, db.ForeignKey('notes.id'), nullable=False, index=True)
    target_note_id = db.Column(db.Integer, db.ForeignKey('notes.id'), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    strength = db.Column(db.Float, default=1.0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)

    __table_args__ = (
        db.UniqueConstraint('source_note_id', 'target_note_id', name='uq_connection_pair'),
    )

    def __repr__(self):
        return f'<Connection {self.source_note_id}->{self.target_note_id}>'
