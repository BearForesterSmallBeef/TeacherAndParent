import datetime
import sqlalchemy
from sqlalchemy import orm
from app import db


class Object(db.Model):
    __tablename__ = 'objects'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    name = db.Column(db.String, nullable=False)
    about = db.Column(db.String, nullable=True)

    def __repr__(self):
        return '<Object %r>' % "; ".join(map(str, [self.id, self.name]))


class Class(db.Model):
    __tablename__ = 'classes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    name = db.Column(db.String, nullable=False)
    about = db.Column(db.String, nullable=True)

    def __repr__(self):
        return '<Class %r>' % "; ".join(map(str, [self.id, self.name]))


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    name = db.Column(db.String, nullable=False)
    about = db.Column(db.String, nullable=True)

    def __repr__(self):
        return '<Role %r>' % "; ".join(map(str, [self.id, self.name]))


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    login = db.Column(db.String, nullable=False, index=True, unique=True)
    hashed_password = db.Column(db.String, nullable=False, index=True)
    name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False, index=True)
    middle_name = db.Column(db.String, nullable=True)
    role_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("roles.id"), index=True)
    role = orm.relation('Role')
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return '<User %r>' % "; ".join(map(str, [self.id, self.login, self.surname, self.role_id]))


class Parent(db.Model):
    __tablename__ = 'parents'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    parent_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), index=True)
    parent = orm.relation('User')
    class_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("classes.id"), index=True)
    Class = orm.relation('Class')

    def __repr__(self):
        return '<Parent %r>' % "; ".join(map(str, [self.parent_id, self.class_id]))


class TeacherAndTheirObjectsAndClasses(db.Model):
    __tablename__ = 'teachers&objects&classes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    teacher_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), index=True)
    teacher = orm.relation('User')
    object_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("objects.id"), index=True)
    object = orm.relation('Object')
    class_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("classes.id"), index=True)
    Class = orm.relation('Class')

    def __repr__(self):
        return '<TeacherAndTheirObjectsAndClasses %r>' % "; ".join(map(str, [self.id, self.teacher_id, self.object_id,
                                                                             self.class_id]))


class Consultation(db.Model):
    __tablename__ = 'consultations'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    teacher_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), index=True)
    teacher = orm.relation('User')
    parent_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("parents.id"), index=True)
    parent = orm.relation('Parent')
    consultation_start_time = sqlalchemy.Column(sqlalchemy.DateTime)
    duration = sqlalchemy.Column(sqlalchemy.DateTime)
    status = sqlalchemy.Column(sqlalchemy.Boolean, default=True)

    def __repr__(self):
        return '<Consultation %r>' % "; ".join(map(str, [self.id, self.teacher_id, self.parent_id, self.status,
                                                  self.consultation_start_time, self.duration]))

# TODO разобраться с миграциями +
# TODO заполнение тестовами данными
# TODO Формочка для админа
# TODO разобраться c login`ами и role`ами
