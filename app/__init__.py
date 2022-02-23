import os
from flask import Flask


def create_app():
    app = Flask(__name__)
    CONFIG_TYPE = os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig')
    app.config.from_object(CONFIG_TYPE)

    from .views.main import main
    app.register_blueprint(main)

    return app
