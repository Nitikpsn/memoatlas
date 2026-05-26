from datetime import datetime, timezone
import hashlib
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    avatar_url = db.Column(db.String(500), nullable=True)

    # this connects a user to all their notes
    notes = db.relationship('Note', backref='author', lazy=True)

    def set_password(self, password):
        """hash and store the password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """check if the password matches the hash"""
        return check_password_hash(self.password_hash, password)

    def get_avatar(self):
        """return the profile pic or a default gravatar"""
        if self.avatar_url:
            return self.avatar_url
        email_hash = hashlib.md5(self.email.lower().encode()).hexdigest()
        return "https://www.gravatar.com/avatar/" + email_hash + "?s=200&d=identicon"

    def __repr__(self):
        return '<User ' + self.username + '>'
