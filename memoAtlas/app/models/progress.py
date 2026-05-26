from datetime import datetime
from . import db

class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    xp = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return "Progress(user_id='" + str(self.user_id) + "', xp=" + str(self.xp) + ", level=" + str(self.level) + ")"
