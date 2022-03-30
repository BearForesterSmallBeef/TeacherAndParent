import datetime

import sqlalchemy
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class Subject(db.Model):
    __tablename__ = 'subjects'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    name = db.Column(db.String, nullable=False)
    about = db.Column(db.String, nullable=True)

    def __repr__(self):
        return '<Subject %r>' % "; ".join(map(str, [self.id, self.name]))


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


class RolesIds:
    ADMIN = 1
    HEAD_TEACHER = 2
    TEACHER = 3
    PARENT = 4


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    login = db.Column(db.String, index=True, unique=True, nullable=True)
    hashed_password = db.Column(db.String, index=True, nullable=True)
    name = db.Column(db.String, nullable=True)
    surname = db.Column(db.String, index=True, nullable=True)
    middle_name = db.Column(db.String, nullable=True)
    role_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("roles.id"), index=True,
                                nullable=True)
    role = orm.relation('Role')
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now,
                                     nullable=True)

    @property
    def password(self):
        # https://github.com/miguelgrinberg/flasky/blob/master/app/models.py#L129
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def full_name(self):
        return f"{self.surname} {self.name} {self.middle_name}"

    def __repr__(self):
        return '<User %r>' % "; ".join(map(str, [self.id, self.login, self.surname, self.role_id]))


class Parent(db.Model):
    __tablename__ = 'parents'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), index=True)
    user = orm.relation('User')
    class_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("classes.id"), index=True)
    class_ = orm.relation('Class')

    def __repr__(self):
        return '<Parent %r>' % "; ".join(map(str, [self.user_id, self.class_id]))


class TeacherSubjectsClasses(db.Model):
    __tablename__ = 'teacher_subjects_classes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    teacher_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), index=True)
    teacher = orm.relation('User')
    subject_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("subjects.id"),
                                   index=True)
    subject = orm.relation('Subject')
    class_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("classes.id"), index=True)
    class_ = orm.relation('Class')

    def __repr__(self):
        return '<TeacherSubjectsClasses %r>' % "; ".join(
            map(str, [self.id, self.teacher_id, self.subject_id,
                      self.class_id]))


class Consultation(db.Model):
    __tablename__ = 'consultations'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    teacher_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), index=True)
    teacher = orm.relation(User, foreign_keys=teacher_id)
    parent_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), index=True)
    parent = orm.relationship(User, foreign_keys=parent_id)
    date = sqlalchemy.Column(sqlalchemy.Date)
    start_time = sqlalchemy.Column(sqlalchemy.Time)
    finish_time = sqlalchemy.Column(sqlalchemy.Time)
    status = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    url = sqlalchemy.Column(sqlalchemy.String)

    @property
    def duration(self):
        return (datetime.datetime.combine(datetime.date.min,
                                          self.finish_time)
                - datetime.datetime.combine(datetime.date.min,
                                            self.start_time)).seconds

    def __repr__(self):
        return '<Consultation %r>' % "; ".join(
            map(str, [self.id, self.teacher_id, self.parent_id, self.status,
                      self.start_time, self.finish_time]))

# TODO Формочка для админа
# TODO разобраться c login`ами и role`ами
