from ..models.note import Note

def get_graph_data(user_id):
    """Converts user notes into a format suitable for D3.js or Vis.js"""
    notes = Note.query.filter_by(user_id=user_id).all()
    
    nodes = []
    links = []
    
    for note in notes:
        nodes.append({
            "id": note.id,
            "title": note.title,
            "group": 1,
            "updated_at": (note.updated_at or note.date_posted).isoformat()
        })
        
        for other_note in notes:
            if note.id != other_note.id and note.date_posted.date() == other_note.date_posted.date():
                links.append({
                    "source": note.id,
                    "target": other_note.id,
                    "value": 1
                })
                
    return {"nodes": nodes, "links": links} 