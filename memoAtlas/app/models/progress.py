from app import db
from datetime import datetime

class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    xp = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"Progress(user_id='{self.user_id}', xp={self.xp}, level={self.level})"
