from flask import Flask


def create_app(config_type):
    app = Flask(__name__)
    app.config.from_object(config_type)

    from .views.main import main
    from .views.auth import auth
    app.register_blueprint(main)
    app.register_blueprint(auth)

    return app
