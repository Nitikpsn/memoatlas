from ..models.note import Note
from ..models.connection import Connection
from ..models.user import db
from datetime import datetime

def get_graph_data(user_id):
    notes = Note.query.filter_by(user_id=user_id).all()

    nodes = []
    links = []

    for note in notes:
        nodes.append({
            "id": note.id,
            "title": note.title,
            "group": 1,
            "is_matched": note.is_matched,
            "updated_at": (note.updated_at or note.date_posted).isoformat()
        })

        for other_note in notes:
            if note.id != other_note.id and note.date_posted.date() == other_note.date_posted.date():
                links.append({
                    "source": note.id,
                    "target": other_note.id,
                    "value": 1
                })

    user_connections = Connection.query.filter_by(user_id=user_id).all()
    for conn in user_connections:
        links.append({
            "source": conn.source_note_id,
            "target": conn.target_note_id,
            "value": 1,
            "manual": True
        })

    return {"nodes": nodes, "links": links}


class GraphService:

    @staticmethod
    def create_connection(user_id, source_note_id, target_note_id, relationship_type=None):
        existing = Connection.query.filter(
            ((Connection.source_note_id == source_note_id) & (Connection.target_note_id == target_note_id)) |
            ((Connection.source_note_id == target_note_id) & (Connection.target_note_id == source_note_id))
        ).first()
        if existing:
            return existing

        conn = Connection(
            source_note_id=source_note_id,
            target_note_id=target_note_id,
            user_id=user_id,
            relationship_type=relationship_type
        )
        db.session.add(conn)

        source_note = db.session.get(Note, source_note_id)
        target_note = db.session.get(Note, target_note_id)
        if source_note:
            source_note.is_matched = True
        if target_note:
            target_note.is_matched = True

        db.session.commit()
        return conn

    @staticmethod
    def get_connected_notes(note_id, user_id):
        conns = Connection.query.filter(
            (Connection.source_note_id == note_id) | (Connection.target_note_id == note_id),
            Connection.user_id == user_id
        ).all()
        connected = []
        for c in conns:
            other_id = c.target_note_id if c.source_note_id == note_id else c.source_note_id
            note = db.session.get(Note, other_id)
            if note:
                connected.append(note)
        return connected
