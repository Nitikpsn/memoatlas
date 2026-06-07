import os
from dotenv import load_dotenv

load_dotenv()

from memoatlas import create_app

app = create_app()
