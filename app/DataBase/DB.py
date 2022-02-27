from flask_sqlalchemy import SQLAlchemy
import datetime
import sqlalchemy
from sqlalchemy import orm
from app import db
from app import create_app
import os

app = create_app(os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig'))


def creating_bd_file(db):
    db.create_all()


class School(db.Model):
    __tablename__ = 'schools'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    name = db.Column(db.String, nullable=False)
    about = db.Column(db.String, nullable=True)

    def __repr__(self):
        return '<School %r>' % self.id


class Object(db.Model):
    __tablename__ = 'objects'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    name = db.Column(db.String, nullable=False)
    about = db.Column(db.String, nullable=True)

    def __repr__(self):
        return '<Object %r>' % self.id


class Classes(db.Model):
    __tablename__ = 'classes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    name = db.Column(db.String, nullable=False)
    about = db.Column(db.String, nullable=True)

    def __repr__(self):
        return '<Class %r>' % self.id


class Status(db.Model):
    __tablename__ = 'statuses'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    name = db.Column(db.String, nullable=False, index=True)
    about = db.Column(db.String, nullable=True)

    def __repr__(self):
        return '<Status %r>' % self.id


class Admin(db.Model):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False, index=True)
    middle_name = db.Column(db.String, nullable=True)
    School_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("schools.id"), index=True)
    School = orm.relation('School')
    Status_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("statuses.id"))
    Status = orm.relation('Status')

    def __repr__(self):
        return '<Admin %r>' % self.id


class Teacher(db.Model):
    __tablename__ = 'teachers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False, index=True)
    middle_name = db.Column(db.String, nullable=True)
    School_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("schools.id"), index=True)
    School = orm.relation('School')
    Status_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("statuses.id"))
    Status = orm.relation('Status')
    Classes = db.Column(db.String, nullable=False)
    Objects = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<Teacher %r>' % self.id


class Parent(db.Model):
    __tablename__ = 'parents'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False, index=True)
    middle_name = db.Column(db.String, nullable=True)
    Status_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("statuses.id"))
    Status = orm.relation('Status')

    def __repr__(self):
        return '<Parent %r>' % self.id


class Child(db.Model):
    __tablename__ = 'children'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False, index=True)
    middle_name = db.Column(db.String, nullable=True)
    School_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("schools.id"), index=True)
    School = orm.relation('School')
    Status_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("statuses.id"))
    Status = orm.relation('Status')
    Class_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("classes.id"), index=True)
    Classes = orm.relation('Classes')
    Classroom_teacher_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("teachers.id"), index=True)
    Classroom_teacher = orm.relation('Teacher')
    Parents = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<Child %r>' % self.id


with app.app_context():
    creating_bd_file(db)
