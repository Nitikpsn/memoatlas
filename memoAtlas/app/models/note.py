from datetime import datetime
from . import db

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    tags = db.Column(db.String(500), nullable=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_matched = db.Column(db.Boolean, default=False)
    last_revised = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    health_score = db.Column(db.Integer, default=20)

    def get_tag_list(self):
        if not self.tags:
            return []
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]

    def wither_days(self):
        delta = datetime.utcnow() - self.last_revised
        return delta.days

    def is_wilted(self):
        return self.wither_days() >= 30

    def effective_health(self):
        if self.wither_days() >= 30:
            return max(0, self.health_score - self.wither_days())
        return self.health_score

    def __repr__(self):
        return "Note('"+self.title+"', '"+str(self.date_posted)+"')"
