import os
from flask import Flask
from flask_login import LoginManager
from config import Config
from .models.user import db

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models.user import User
    from .models.connection import Connection
    from .models.progress import Progress
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .routes.main import main
    from .routes.auth import auth
    from .routes.notes import notes
    from .routes.graph import graph
    from .routes.api import api
    from .routes.search import search_bp
    from .routes.user import user_bp
    from .routes.game import game

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(notes)
    app.register_blueprint(graph)
    app.register_blueprint(api)
    app.register_blueprint(search_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(game)

    with app.app_context():
        db.create_all()

    return app