from datetime import timedelta

from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from flask_apispec import FlaskApiSpec
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_jwt_extended import JWTManager


bootstrap = Bootstrap5()
metadata = MetaData(
  naming_convention={
    'pk': 'pk_%(table_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'ix': 'ix_%(table_name)s_%(column_0_name)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    }
)
db = SQLAlchemy(metadata=metadata)
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = "Вы не авторизованы. Пожалуйста, войдите."
login_manager.login_message_category = "error"
ma = Marshmallow()
docs = FlaskApiSpec()
spec = APISpec(
    title="Consultations",
    version="0.0.1",
    openapi_version="2.0",
    info=dict(description="Api for interaction with TeacherAndParent app"),
    plugins=[MarshmallowPlugin()]
)
jwt = JWTManager()


def create_app(config_type):
    app = Flask(__name__)
    app.config.from_object(config_type)
    app.config["APISPEC_SPEC"] = spec
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    login_manager.init_app(app)
    ma.init_app(app)
    docs.init_app(app)
    jwt.init_app(app)

    from .main.views import main
    from .auth.views import auth
    from .api import api_bp
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(api_bp)

    return app
