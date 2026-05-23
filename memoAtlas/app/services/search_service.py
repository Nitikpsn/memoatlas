from ..models.note import Note

def search_notes(user_id, query):
    if not query:
        return []
    return Note.query.filter(
        Note.user_id == user_id,
        (Note.title.ilike(f'%{query}%')) | (Note.content.ilike(f'%{query}%'))
    ).all()
