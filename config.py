import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
APP_NAME = "app"
APP_DIR = os.path.join(BASE_DIR, APP_NAME)


class Config:
    SECRET_KEY = (os.environ.get('SECRET_KEY') or
                  'b67e72537cd64362f5d62961e6e94dcd265a6604af0d446723ddde174ceb480b')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    TESTING = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://user@localhost/db.sqlite'


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'db.sqlite')}"


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
