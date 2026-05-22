import os

# This finds the absolute path of your memoAtlas folder
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # SECRET_KEY protects your login/register forms from CSRF attacks
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'atlas-brain-secret-key-99'
    
    # SQLALCHEMY_DATABASE_URI tells Flask where to create your database file
    # This will create 'memoatlas.db' right inside your main folder
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'memoatlas.db')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False 