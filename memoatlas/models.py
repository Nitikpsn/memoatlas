from datetime import datetime
import hashlib
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    avatar_url = db.Column(db.String(500), nullable=True)
    trees = db.relationship('Tree', backref='author', lazy=True, cascade='all, delete-orphan')
    progress = db.relationship('Progress', uselist=False, backref='user', cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_avatar(self):
        if self.avatar_url:
            return self.avatar_url
        h = hashlib.md5(self.email.lower().encode()).hexdigest()
        return "https://www.gravatar.com/avatar/" + h + "?s=200&d=identicon"


class Tree(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    tags = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    last_revised = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    health_score = db.Column(db.Integer, default=20)

    def get_tag_list(self):
        if not self.tags:
            return []
        return [t.strip() for t in self.tags.split(',') if t.strip()]

    def days_unrevised(self):
        delta = datetime.utcnow() - self.last_revised
        return delta.days

    def get_effective_health(self):
        days = self.days_unrevised()
        if days <= 30:
            return self.health_score
        decay = days - 30
        return max(0, self.health_score - decay)

    def get_stage(self):
        health = self.get_effective_health()
        days = self.days_unrevised()
        if days > 60 or health <= 0:
            return 'dead'
        if days > 45:
            return 'wilting'
        if days > 30:
            return 'fading'
        if health <= 20:
            return 'seed'
        if health <= 40:
            return 'sprout'
        if health <= 70:
            return 'young'
        if health <= 90:
            return 'mature'
        return 'ancient'

    def needs_care(self):
        return self.days_unrevised() > 25


class Connection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source_id = db.Column(db.Integer, db.ForeignKey('tree.id'), nullable=False)
    target_id = db.Column(db.Integer, db.ForeignKey('tree.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    source = db.relationship('Tree', foreign_keys=[source_id])
    target = db.relationship('Tree', foreign_keys=[target_id])


class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    xp = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
