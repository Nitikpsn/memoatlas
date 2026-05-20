from app.models.note import Note
from sqlalchemy import or_


class SearchService:

    @staticmethod
    def search_notes(user_id, query, subject=None, tag=None):
        base_query = Note.query.filter_by(user_id=user_id)

        if query:
            search_pattern = f'%{query}%'
            base_query = base_query.filter(
                or_(
                    Note.title.ilike(search_pattern),
                    Note.content.ilike(search_pattern),
                    Note.tags.ilike(search_pattern)
                )
            )

        if subject:
            base_query = base_query.filter(Note.subject.ilike(f'%{subject}%'))

        if tag:
            base_query = base_query.filter(Note.tags.ilike(f'%{tag}%'))

        return base_query.order_by(Note.updated_at.desc()).all()

    @staticmethod
    def get_subjects(user_id):
        subjects = (
            Note.query
            .filter_by(user_id=user_id)
            .with_entities(Note.subject)
            .distinct()
            .all()
        )
        return [s[0] for s in subjects if s[0]]

    @staticmethod
    def get_all_tags(user_id):
        notes = Note.query.filter_by(user_id=user_id).all()
        tag_set = set()
        for note in notes:
            tag_set.update(note.tag_list)
        return sorted(tag_set)

    @staticmethod
    def suggest_connections(user_id, note_id, limit=5):
        note = Note.query.filter_by(id=note_id, user_id=user_id).first()
        if not note:
            return []

        from app.models.connection import Connection
        existing_connections = (
            Connection.query
            .filter_by(user_id=user_id)
            .filter(
                (Connection.source_note_id == note_id) | (Connection.target_note_id == note_id)
            )
            .with_entities(Connection.source_note_id, Connection.target_note_id)
            .all()
        )
        connected_ids = set()
        for src, tgt in existing_connections:
            if src == note_id:
                connected_ids.add(tgt)
            else:
                connected_ids.add(src)

        candidates = (
            Note.query
            .filter(
                Note.user_id == user_id,
                Note.id != note_id,
                Note.id.notin_(connected_ids) if connected_ids else True
            )
            .filter(
                or_(
                    Note.subject == note.subject,
                    Note.tags.ilike(f'%{note.tags}%') if note.tags else False
                )
            )
            .limit(limit)
            .all()
        )

        return candidates
