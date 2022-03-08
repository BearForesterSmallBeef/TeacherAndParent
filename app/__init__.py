from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import *


bootstrap = Bootstrap5()
db = SQLAlchemy()
migrate = Migrate()


def create_app(config_type):
    app = Flask(__name__)
    app.config.from_object(config_type)

    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    init(directory='.\\app\\models\\migrations', multidb=False)

    from .views.main import main
    from .views.auth import auth
    app.register_blueprint(main)
    app.register_blueprint(auth)

    return app
