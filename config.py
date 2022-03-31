import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
APP_NAME = "app"
APP_DIR = os.path.join(BASE_DIR, APP_NAME)


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'strong secret key'
    FLASK_APP = os.environ.get('FLASK_APP')
    SERVER_NAME = f'{os.environ.get("SERVER_NAME", "127.0.0.1")}:{os.environ.get("FLASK_RUN_PORT")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    TESTING = False


class ProductionConfig(Config):
    FLASK_ENV = 'production'
    SQLALCHEMY_DATABASE_URI = 'mysql://user@localhost/db.sqlite'


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'db.sqlite')}"
