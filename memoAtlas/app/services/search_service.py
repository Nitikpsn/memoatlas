from ..models.note import Note

def search_notes(user_id, query):
    """search a user's notes by title or content"""
    if not query:
        return []
    return Note.query.filter(
        Note.user_id == user_id,
        (Note.title.ilike('%' + query + '%')) | (Note.content.ilike('%' + query + '%'))
    ).all()
