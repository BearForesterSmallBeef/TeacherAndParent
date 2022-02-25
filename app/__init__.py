from flask import Flask


def create_app(config_type):
    app = Flask(__name__)
    app.config.from_object(config_type)

    from .views.main import main
    app.register_blueprint(main)

    return app
