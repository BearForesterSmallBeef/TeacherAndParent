from flask import Flask
from flask_bootstrap import Bootstrap5


bootstrap = Bootstrap5()


def create_app(config_type):
    app = Flask(__name__)
    app.config.from_object(config_type)

    bootstrap.init_app(app)

    from .views.main import main
    from .views.auth import auth
    app.register_blueprint(main)
    app.register_blueprint(auth)

    return app
