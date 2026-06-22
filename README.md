# MemoAtlas

I built this as my first real software project. I wanted a note-taking app that didn't feel like a bunch of dead text files sitting in folders. So I made one where each note is a tree in a forest, and the forest lives or dies based on how often you revisit what you wrote.

Live demo: https://memoatlas.vercel.app/

## What it does

- Write notes (they're called trees)
- Link related notes together to build a knowledge graph
- Revise notes to keep them alive — if you ignore a tree too long, it dies and becomes a stump
- Earn XP by making connections between ideas
- A pulsing graph shows you where your attention has been vs. what you're neglecting

Notes go through life stages: Seed → Sprout → Young → Mature → Ancient. Neglected ones fade and eventually die.

## Tech I used

- Python + Flask for the backend
- SQLite (with Flask-SQLAlchemy)
- Vis.js for the graph visualization
- Plain CSS and JavaScript (no frameworks)
- Deployed on Vercel

## Challenges I faced

The hardest part was getting the graph to work properly. I had never used Vis.js before, so figuring out how to make nodes pulse based on revision data took a lot of trial and error. The data format the library expected was different from what I was sending, and I kept getting blank graphs for hours until I realized my JSON structure was wrong.

I also struggled with the health decay logic. Getting the timing right — when does a tree start wilting, how many days without revision triggers decay — took several rewrites. I originally made the decay too aggressive and all my test trees died in a week.

Deployment on Vercel was another headache. Flask + serverless doesn't play well with SQLite out of the box, and I had to figure out the temp directory setup for the database file.

## What I learned

- How sessions and authentication work in Flask
- Basic graph theory and Jaccard similarity for the connection recommendations
- That CSS without a framework is both freeing and painful
- How to debug serverless deployments

## Setup

```
git clone https://github.com/Nitikpsn/memoatlas.git
cd memoatlas
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py
```

Needs a `SECRET_KEY` environment variable (see `.env.example`).

## What's next

- Better search
- User accounts (it's single-user right now on the live site)
- Maybe PostgreSQL support for real persistence

Thanks for checking it out.
