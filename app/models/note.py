from .user import db
from datetime import datetime

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationships
    author = db.relationship('User', backref=db.backref('notes', lazy=True))

class Connection(db.Model):
    """Links two notes together (the 'edges' in your graph)"""
    id = db.Column(db.Integer, primary_key=True)
    from_note_id = db.Column(db.Integer, db.ForeignKey('note.id'), nullable=False)
    to_note_id = db.Column(db.Integer, db.ForeignKey('note.id'), nullable=False)