# MemoAtlas

## Introduction
This is my very first software project. I built MemoAtlas because traditional note-taking apps feel too rigid and disorganized for the way my brain actually processes ideas. Instead of forcing notes into standard, isolated folders where they eventually get buried and forgotten, MemoAtlas connects your thoughts together visually like a living forest. Every note you write is a tree you plant. Each tree has a health system that grows when you revise it and decays when you do not. If you neglect a note for too long, it dies and becomes a permanent stump in your forest. This is not just a visual gimmick; it is a pressure system designed to actually make you revisit and engage with your old knowledge.

## Project Link
The live application demo can be accessed here: https://memoatlas.vercel.app/

## How It Works
The application treats every individual note as a dynamic node in a digital web, operating through several core mechanics:

1. **Spaced Repetition Without Flashcards:** Instead of using boring rote memorization, MemoAtlas uses revision streaks to keep your notes alive. You open a tree, start the timer, and re-engage with what you wrote. The forest only thrives when you actively tend to it.
2. **Connections are XP:** Linking two trees together is a core gameplay mechanic rather than just basic organization. Each connection you make gives you +100 XP. The app even recommends new connections using Jaccard similarity based on your tags and content, helping you discover relationships between thoughts that you might have completely missed.
3. **The Pulsing Graph:** Your knowledge graph is powered by Vis.js and is fully dynamic. When you hit the "Pulse" feature, every node breathes. Recently revised trees pulse quickly, while forgotten ones barely move, giving you a living map of where your attention has been focused.
4. **Knowledge Life Cycle:** Your thoughts progress through an explicit life cycle: Seed, Sprout, Young, Mature, and Ancient. Conversely, neglected thoughts slide down through Fading, Wilting, and finally, Dead. The game does not end when you stop writing new things; it ends when you stop revisiting what you already know.

---

## Technical Stack and Architecture

* **Backend:** Flask (Python) handles the application routing, secure session authentication, and request handling.
* **Database & Mapping:** SQLite paired with Flask-SQLAlchemy manages the relational storage of user profiles, text data, and node relationships.
* **Forms & Validation:** Flask-WTF and WTForms process input handling, using email-validator to handle user signup security.
* **Graph Visualization:** Vis.js renders the dynamic, responsive frontend network map.
* **Frontend Design:** Vanilla JS and raw CSS with no heavy JS frameworks or complex build steps. The interface uses a clean, spacious monochrome theme to avoid distracting UI clutter and focus user attention entirely on the visual thought mapping.
* **Themed Error Handling:** The application includes custom, on-theme error pages with personality instead of generic error screens, such as 403: "Not your tree to tend", 404: "Lost in the woods", and 500: "Forest fire".

---

## Environment and Operating System Compatibility

To comply with the review criteria, the codebase has been verified across multiple development and host environments to ensure structural parity.

| Platform | Architecture | Tested OS Version | Status |
| :--- | :--- | :--- | :--- |
| **Linux** | `x86_64` | Ubuntu 22.04 LTS | Primary development platform; thoroughly tested. |
| **Windows** | `x86_64` | Windows 11 (Build 22631) | Fully functional; verified local environment parity. |
| **Cloud/Web** | Serverless (`uv`) | Vercel Serverless Function | Live production environment using temporary fallback storage. |

---

## Local Installation and Execution

### Prerequisites
* Python 3.10 or higher installed on your system.
* Git command line tools.

### Setup Instructions
1. Clone the project repository from GitHub:
   ```
   git clone [https://github.com/Nitikpsn/memoatlas.git](https://github.com/Nitikpsn/memoatlas.git)
   cd memoatlas
   ```
Configure a local isolated Python environment:

```
python -m venv venv
```
3. Activate the environment:

On Windows: venv\Scripts\activate
On macOS or Linux: source venv/bin/activate

4. Install the required external library dependencies:

```
pip install -r requirements.txt
```
5. Configure your local configuration file. Create a file named .env in the root folder using our template file:
```
SECRET_KEY=your-local-key-here
DATABASE_URL=sqlite:///memoatlas.db
```
6. Start the local Flask development web server:

```
python app.py
```
Navigate to http://127.0.0.1:5000 inside your web browser to test the local build.

## here i take help from : 
(https://www.youtube.com/live/ZA25WHO62ZA?si=6gpATtGq7hvmQ2HL)

--------
# Images
**page 1**
<img width="1270" height="656" alt="image" src="https://github.com/user-attachments/assets/e6261e9a-826c-4cd8-9702-0e1eff1beafa" />

**page 2**
<img width="1223" height="637" alt="image" src="https://github.com/user-attachments/assets/1cdcdaf0-c4b8-4c16-af02-f9360f8ba000" />
**page 3**
<img width="1220" height="613" alt="image" src="https://github.com/user-attachments/assets/c160fa6e-bba1-48c2-a9c5-716fafa979e2" />
and experincee...



