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


class Admin(db.Model):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False, index=True)
    middle_name = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=False, index=True, unique=True)
    hashed_password = db.Column(db.String, nullable=False, index=True)
    School_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("schools.id"), index=True)
    School = orm.relation('School')
    Сreated_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return '<Admin %r>' % self.id


class Teacher(db.Model):
    __tablename__ = 'teachers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False, index=True)
    middle_name = db.Column(db.String, nullable=True)
    login = db.Column(db.String, nullable=False, index=True, unique=True)
    hashed_password = db.Column(db.String, nullable=False, index=True)
    School_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("schools.id"), index=True)
    School = orm.relation('School')
    Сreated_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return '<Teacher %r>' % self.id


class Parent(db.Model):
    __tablename__ = 'parents'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    name = db.Column(db.String)
    surname = db.Column(db.String, index=True)
    middle_name = db.Column(db.String, nullable=True)
    login = db.Column(db.String, index=True, unique=True)
    hashed_password = db.Column(db.String, index=True)
    School_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("schools.id"), index=True)
    School = orm.relation('School')
    authorized = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    Class_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("classes.id"), index=True)
    Classes = orm.relation('Classes')
    Сreated_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return '<Parent %r>' % self.id


class Consultation(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    teacher_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("teachers.id"), index=True)
    teacher = orm.relation('Teacher')
    # parent_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("teachers.id"), index=True)
    is_free = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    start_time = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
    finish_time = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
    duration = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)


class TeacherAndClassesAndObjects(db.Model):
    __tablename__ = 'teacher_and_classes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    teacher_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("teachers.id"), index=True)
    teacher = orm.relation('Teacher')
    parent_id
    parent
    Class_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("classes.id"), index=True)
    Classes = orm.relation('Classes')
    object_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("objects.id"), index=True)
    object = orm.relation('Object')


with app.app_context():
    creating_bd_file(db)


# TODO разобраться с миграциями
# TODO заполнение тестовами данными
# TODO Формочка для админа
# TODO разобраться c login`ами и rile`ами


