from app.models.note import Note
from app.models.connection import Connection


class GraphService:

    @staticmethod
    def get_graph_data(user_id):
        notes = Note.query.filter_by(user_id=user_id).all()
        connections = Connection.query.filter_by(user_id=user_id).all()

        nodes = [
            {
                'id': note.id,
                'label': note.title,
                'subject': note.subject or 'uncategorized',
                'tags': note.tag_list,
            }
            for note in notes
        ]

        edges = [
            {
                'source': conn.source_note_id,
                'target': conn.target_note_id,
                'label': conn.description or '',
                'strength': conn.strength,
            }
            for conn in connections
        ]

        return {'nodes': nodes, 'edges': edges}

    @staticmethod
    def get_connected_notes(note_id, user_id):
        connections = Connection.query.filter(
            Connection.user_id == user_id,
            (Connection.source_note_id == note_id) | (Connection.target_note_id == note_id)
        ).all()

        connected_notes = set()
        for conn in connections:
            if conn.source_note_id == note_id:
                connected_notes.add(conn.target_note_id)
            else:
                connected_notes.add(conn.source_note_id)

        return Note.query.filter(Note.id.in_(connected_notes)).all() if connected_notes else []

    @staticmethod
    def create_connection(user_id, source_id, target_id, description=None, strength=1.0):
        from app import db

        existing = Connection.query.filter_by(
            user_id=user_id,
            source_note_id=source_id,
            target_note_id=target_id
        ).first()
        if existing:
            return existing

        source_note = Note.query.filter_by(id=source_id, user_id=user_id).first()
        target_note = Note.query.filter_by(id=target_id, user_id=user_id).first()
        if not source_note or not target_note:
            return None

        connection = Connection(
            user_id=user_id,
            source_note_id=source_id,
            target_note_id=target_id,
            description=description,
            strength=strength
        )
        db.session.add(connection)
        db.session.commit()
        return connection

    @staticmethod
    def remove_connection(user_id, connection_id):
        from app import db

        connection = Connection.query.filter_by(
            id=connection_id,
            user_id=user_id
        ).first()
        if connection:
            db.session.delete(connection)
            db.session.commit()
            return True
        return False
