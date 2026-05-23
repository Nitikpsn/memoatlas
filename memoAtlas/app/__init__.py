import os
from flask import Flask
from flask_login import LoginManager
from config import Config
from .models.user import db

def create_app():
    app = Flask(__name__)
    
    # Load settings from config.py (Replaces manual config keys)
    app.config.from_object(Config)

    # Initialize Database
    db.init_app(app)

    # Initialize Login Management
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models.user import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Import Blueprints
    from .routes.main import main
    from .routes.auth import auth
    from .routes.notes import notes
    from .routes.dashboard import dashboard
    from .routes.graph import graph
    from .routes.api import api
    from .routes.search import search_bp

    # Register Blueprints
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(notes)
    app.register_blueprint(dashboard)
    app.register_blueprint(graph)
    app.register_blueprint(api)
    app.register_blueprint(search_bp)

    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

    return app