from application import app
from flask_sqlalchemy import SQLAlchemy
from app import db


def creating_bd_file(db):
    db.create_all()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<User %r>' % self.id


creating_bd_file(db)
