from app.models import *  # https://stackoverflow.com/a/57789224
from app import create_app
from app import db
import os

app = create_app(os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig'))

with app.app_context():
    db.session.commit()
