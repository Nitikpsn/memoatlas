from app import db
from datetime import datetime, timezone


class Note(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    subject = db.Column(db.String(100), nullable=True, index=True)
    tags = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)

    connections_as_source = db.relationship(
        'Connection',
        foreign_keys='Connection.source_note_id',
        backref='source_note',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    connections_as_target = db.relationship(
        'Connection',
        foreign_keys='Connection.target_note_id',
        backref='target_note',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    @property
    def tag_list(self):
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
        return []

    @tag_list.setter
    def tag_list(self, value):
        self.tags = ','.join(value) if value else None

    def __repr__(self):
        return f'<Note {self.title}>'
