import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config=None):
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'sqlite:///memoatlas.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'

    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return db.session.get(User, int(user_id))

    from app.routes.main import main
    from app.routes.auth import auth
    from app.routes.notes import notes
    from app.routes.dashboard import dashboard
    from app.routes.graph import graph_bp
    from app.routes.api import api

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(notes)
    app.register_blueprint(dashboard)
    app.register_blueprint(graph_bp)
    app.register_blueprint(api)

    with app.app_context():
        db.create_all()

    return app
