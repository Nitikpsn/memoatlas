# MemoAtlas 🧠🌐


**MemoAtlas** is a visual "Second Brain" platform designed to map the atlas of your thoughts.

---

## 🚀 Vision
Turn scattered thoughts into a structured network. Whether you are a student, researcher, or developer, MemoAtlas helps you find hidden patterns in your data through interactive link analysis.

## ✨ Core Features
* **Knowledge Graph**: Dynamic 2D network visualization powered by **Vis.js**.
* **Smart Dashboard**: Real-time tracking of Node counts and Connection density.
* **Secure Auth**: User-specific "Gardens" protected by Flask-Login and Werkzeug.
* **Clean Architecture**: Blueprint-driven Flask setup for high maintainability.

---

## 📂 Project Roadmap & Structure
> **CRITICAL:** This project is case-sensitive. To maintain accurate **Hackatime/WakaTime** stats, always operate within the `memoAtlas/` (CamelCase) root.

```text
memoAtlas/
├── app/
│   ├── models/         # note.py (Model), user.py (Model)
│   ├── routes/         # auth.py, notes.py, dashboard.py, graph.py
│   ├── static/         # Custom CSS & Vis.js Graph Logic
│   └── templates/      # Obsidian-themed Jinja2 templates
├── run.py              # Application Entry Point
└── .venv/              # Isolated Environment
🛠️ Tech Stack
Backend: Python 3.12 / Flask

Database: SQLAlchemy / SQLite

Frontend: Custom CSS / Vis.js

Forms: Flask-WTF

🛠️ Quick Start
Initialize Environment:

Bash


python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
Setup Database:

Bash


python3 -c "from app import create_app, db; app=create_app(); app.app_context().push(); db.create_all()"
Run Application:

Bash


python3 run.py
🤝 Contributing
Contributions are welcome! Please ensure all file names follow the snake_case.py convention to avoid Linux import conflicts.

⚖️ License
Distributed under the MIT License.


### **Pro-Tip for your GitHub Repo:**
To get that "Obsidian" look on the actual GitHub page, you can upload one of those screenshots you showed me (like the Graph view) to your repo and add it to the top of the README like this:
`![Graph Preview](./app/static/img/preview.png)`

**Does this Markdown code cover everything you need for the initial launch?**