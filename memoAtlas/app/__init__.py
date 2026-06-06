from flask import Flask, render_template
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from ..config import Config
from .models import db, User

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
csrf = CSRFProtect()


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)

    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    from .routes.auth import auth
    from .routes.forest import forest
    from .routes.graph import graph
    from .routes.api import api

    app.register_blueprint(auth)
    app.register_blueprint(forest)
    app.register_blueprint(graph)
    app.register_blueprint(api)

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template('errors/500.html'), 500

    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            app.logger.warning(f"Could not create database tables: {e}")

    return app