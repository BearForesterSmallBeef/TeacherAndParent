import datetime
import sqlalchemy
from sqlalchemy import orm
from app import db


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
    school_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("schools.id"), index=True)
    school = orm.relation('School')
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

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
    school_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("schools.id"), index=True)
    school = orm.relation('School')
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

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
    school_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("schools.id"), index=True)
    school = orm.relation('School')
    authorized = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    class_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("classes.id"), index=True)
    classes = orm.relation('Classes')
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return '<Parent %r>' % self.id


class Consultation(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    teacher_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("teachers.id"), index=True)
    teacher = orm.relation('Teacher')
    parent_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("parents.id"), index=True)
    parent = orm.relation('Parent')
    is_free = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    start_time = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
    finish_time = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
    duration = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)


class TeacherAndClassAndObject(db.Model):
    __tablename__ = 'teachers_and_classes_and_objects'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    teacher_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("teachers.id"), index=True)
    teacher = orm.relation('Teacher')
    class_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("classes.id"), index=True)
    classes = orm.relation('Classes')
    object_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("objects.id"), index=True)
    object = orm.relation('Object')


# TODO разобраться с миграциями +
# TODO заполнение тестовами данными
# TODO Формочка для админа
# TODO разобраться c login`ами и role`ами
