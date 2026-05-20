# MemoAtlas

**Visual knowledge mapping platform for students.**

MemoAtlas is a Flask-based web application that transforms scattered notes into interactive knowledge graphs, helping students see how concepts connect across subjects. Think of it as a "second brain" that reveals relationships between your ideas.

## Features

- **User Authentication** - Secure registration, login, and logout with password hashing
- **Note Management** - Create, read, update, and delete notes with titles, content, subjects, and tags
- **Knowledge Graph** - Visualize connections between notes as an interactive graph using vis-network
- **Dashboard** - View statistics, recent notes, and activity tracking at a glance
- **Search & Filter** - Search notes by title, content, subject, or tags
- **REST API** - Full JSON API for notes, graph data, connections, and statistics
- **Activity Logging** - Track note creation, updates, and deletions over time

## Tech Stack

- **Backend**: Flask 3.x
- **Database**: SQLAlchemy (SQLite by default, supports any SQLAlchemy-compatible database)
- **Authentication**: Flask-Login with Werkzeug password hashing
- **Forms**: Flask-WTF with WTForms validation
- **Graph Visualization**: vis-network (client-side)
- **Templating**: Jinja2

## Project Structure

```
memoatlas/
├── run.py                  # Application entry point
├── requirements.txt        # Python dependencies
├── .env.example            # Example environment variables
├── app/
│   ├── __init__.py         # Application factory, DB, and login manager setup
│   ├── models/
│   │   ├── user.py         # User model with authentication
│   │   ├── note.py         # Note model with tags and subjects
│   │   ├── connection.py   # Connection model linking notes
│   │   └── progress.py     # Activity/progress tracking
│   ├── routes/
│   │   ├── main.py         # Homepage
│   │   ├── auth.py         # Login, register, logout
│   │   ├── notes.py        # Note CRUD operations
│   │   ├── dashboard.py    # User dashboard
│   │   ├── graph.py        # Knowledge graph visualization
│   │   └── api.py          # REST API endpoints
│   ├── services/
│   │   ├── analytics_service.py   # User stats and activity logging
│   │   ├── graph_service.py       # Graph data and connection management
│   │   └── search_service.py      # Note search and filtering
│   ├── forms/
│   │   ├── login_form.py          # Login form with validation
│   │   ├── register_form.py       # Registration form with uniqueness checks
│   │   └── note_form.py           # Note creation/editing form
│   ├── templates/
│   │   ├── base.html              # Base template with navigation
│   │   ├── index.html             # Landing page
│   │   ├── auth/                  # Login and register pages
│   │   ├── dashboard/             # Dashboard view
│   │   ├── graph/                 # Knowledge graph visualization
│   │   ├── notes/                 # Note list, create, edit, detail
│   │   └── profile/               # User profile
│   └── static/
│       ├── css/                   # Stylesheets
│       └── js/                    # JavaScript files
└── tests/
    ├── test_auth.py               # Authentication tests
    ├── test_notes.py              # Note CRUD tests
    └── test_graph.py              # Graph and connection tests
```

## Quick Start

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager) or [uv](https://docs.astral.sh/uv/) (fast Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Nitikpsn/memoatlas.git
   cd memoatlas
   ```

2. **Set up the environment**

   **Option A: Using uv (recommended, faster)**
   ```bash
   # Install uv if you don't have it
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Create a virtual environment and install dependencies
   uv venv
   source .venv/bin/activate   # On Windows: .venv\Scripts\activate
   uv pip install -r requirements.txt
   ```

   **Option B: Using venv and pip**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and set your `SECRET_KEY` to a secure random string.

4. **Run the application**
   ```bash
   python run.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

## Configuration

MemoAtlas uses environment variables for configuration. Copy `.env.example` to `.env` and customize:

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Secret key for session security | `dev-key-change-in-production` |
| `DATABASE_URI` | SQLAlchemy database URI | `sqlite:///memoatlas.db` |

### Production Database

For production, use a robust database like PostgreSQL:

```bash
DATABASE_URI=postgresql://user:password@localhost/memoatlas
```

## API Reference

All API endpoints require authentication and are prefixed with `/api`.

### Notes

- `GET /api/notes` - List all notes (supports `?q=`, `?subject=`, `?tag=` filters)
- `GET /api/notes/<id>` - Get a single note

### Graph

- `GET /api/graph` - Get graph data (nodes and edges)
- `POST /api/graph/connect` - Create a connection between notes
  ```json
  { "source_id": 1, "target_id": 2, "description": "related to", "strength": 1.0 }
  ```
- `DELETE /api/graph/connect/<id>` - Remove a connection

### Search

- `GET /api/search?q=query&subject=Biology&tag=cells` - Search notes

### Stats

- `GET /api/stats` - Get user statistics (note count, connection count, subject distribution)

## Running Tests

```bash
python -m pytest tests/ -v
```

Or using unittest directly:

```bash
python -m unittest discover tests/
```

With uv:

```bash
uv run python -m unittest discover tests/
```

## Development

### Adding a New Feature

1. Create your model in `app/models/`
2. Add routes in `app/routes/`
3. Register the blueprint in `app/__init__.py`
4. Create templates in `app/templates/`
5. Add tests in `tests/`

### Code Style

This project follows standard Python conventions (PEP 8). Key patterns:

- Application factory pattern (`create_app`)
- Blueprint-based routing with `url_prefix`
- Service layer for business logic
- Flask-WTF for form handling and CSRF protection

## License

MIT License. See [LICENSE](LICENSE) for details.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
