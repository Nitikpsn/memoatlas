from flask import Flask
from flask_login import LoginManager
from config import Config
from .models import db, User

def create_app(test_config=None):
    # create the flask app
    app = Flask(__name__)
    app.config.from_object(Config)

    if test_config:
        app.config.update(test_config)

    # connect the database
    db.init_app(app)

    # set up login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # tell flask how to load a user from the database
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # register all the blueprints (route groups)
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

    # create all the database tables
    with app.app_context():
        db.create_all()

    return app
