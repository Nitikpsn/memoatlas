import os
from flask import Flask
from .models.user import db
from flask_login import LoginManager

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-key-very-secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models.user import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .routes.main import main
    from .routes.auth import auth
    from .routes.notes import notes
    from .routes.dashboard import dashboard
    from .routes.graph import graph
    from .routes.api import api

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(notes)
    app.register_blueprint(dashboard)
    app.register_blueprint(graph)
    app.register_blueprint(api)

    with app.app_context():
        db.create_all()

    return app