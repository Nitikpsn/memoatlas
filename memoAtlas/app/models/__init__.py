from flask_sqlalchemy import SQLAlchemy

# create the database object once and share it everywhere
db = SQLAlchemy()

from .user import User
from .note import Note
from .connection import Connection
from .progress import Progress
