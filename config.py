import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
APP_NAME = "app"
APP_DIR = os.path.join(BASE_DIR, APP_NAME)


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'strong secret key'
    FLASK_APP = os.environ.get('FLASK_APP')
    if _ := os.environ.get("SERVER_NAME"):
        SERVER_NAME = _
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    TESTING = False


class ProductionConfig(Config):
    FLASK_ENV = 'production'
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'db.sqlite')}"
