from flask import Flask

from app.api.views import api
from app.extensions import db, migrate, admin, login_manager, cors


def create_app(testing=False, cli=False):
    """
    Application factory, used to create application
    """
    app = Flask(
        __name__,
        template_folder="./assets/html",
    )
    app.config.from_object("app.config")

    if testing is True:
        app.config["TESTING"] = True

    configure_extensions(app)
    register_blueprints(app)

    return app


def configure_extensions(app):
    """configure flask extensions
    """
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    db.init_app(app)
    migrate.init_app(app, db)

    from app.models.user import User
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter(User.id == int(user_id)).first()

    from app.admin.views import ProtectedIndexView
    admin.init_app(app, url='/admin', index_view=ProtectedIndexView(name="Admin"))

    # Add the admin panel
    with app.app_context():
        pass


def register_blueprints(app):
    """register all blueprints for application
    """
    app.register_blueprint(api.blueprint)
