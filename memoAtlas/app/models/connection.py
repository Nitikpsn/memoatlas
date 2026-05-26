from datetime import datetime
from . import db

class Connection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source_note_id = db.Column(db.Integer, db.ForeignKey('note.id'), nullable=False)
    target_note_id = db.Column(db.Integer, db.ForeignKey('note.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    relationship_type = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    source_note = db.relationship('Note', foreign_keys=[source_note_id])
    target_note = db.relationship('Note', foreign_keys=[target_note_id])

    def __repr__(self):
        return "Connection('" + str(self.source_note_id) + "' -> '" + str(self.target_note_id) + "')"
