from flask import Flask
from flask_login import LoginManager
from config import Config
from .models import db, User

login_manager = LoginManager()
login_manager.login_view = 'auth.login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)

    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    login_manager.init_app(app)

    from .routes.auth import auth
    from .routes.forest import forest
    from .routes.graph import graph
    from .routes.api import api

    app.register_blueprint(auth)
    app.register_blueprint(forest)
    app.register_blueprint(graph)
    app.register_blueprint(api)

    with app.app_context():
        db.create_all()

    return app
