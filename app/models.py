import datetime
from functools import singledispatchmethod

import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


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
    parallel = db.Column(db.Integer, index=True)
    groups = db.Column(db.String, nullable=False)
    about = db.Column(db.String, nullable=True)

    def __repr__(self):
        return '<Class %r>' % "; ".join(map(str, [self.id, self.name]))


class Permissions:
    MAKE_APPOINTMENT = 1
    EDIT_CONSULTATIONS = 2
    MANAGE_PARENTS = 4
    MANAGE_TEACHERS = 8
    MANAGE_HEAD_TEACHER = 16
    MANAGE_OBJECTS = 32


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    name = db.Column(db.String, nullable=False)
    permissions = db.Column(db.Integer)
    about = db.Column(db.String, nullable=True)
    users = orm.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'parent': [Permissions.MAKE_APPOINTMENT],
            'teacher': [Permissions.EDIT_CONSULTATIONS, Permissions.MANAGE_PARENTS,
                        Permissions.MANAGE_OBJECTS],
            'head_teacher': [Permissions.EDIT_CONSULTATIONS, Permissions.MANAGE_PARENTS,
                             Permissions.MANAGE_TEACHERS, Permissions.MANAGE_OBJECTS],
            'admin': [Permissions.EDIT_CONSULTATIONS, Permissions.MANAGE_PARENTS,
                      Permissions.MANAGE_TEACHERS, Permissions.MANAGE_HEAD_TEACHER,
                      Permissions.MANAGE_OBJECTS],
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            db.session.add(role)
        db.session.commit()

    def add_permission(self, perm):
        self.permissions |= perm

    def remove_permission(self, perm):
        self.permissions &= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def __repr__(self):
        return '<Role %r>' % "; ".join(map(str, [self.id, self.name]))


class RolesIds:
    ADMIN = 4
    HEAD_TEACHER = 3
    TEACHER = 2
    PARENT = 1


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    login = db.Column(db.String, index=True, unique=True, nullable=True)
    hashed_password = db.Column(db.String, index=True, nullable=True)
    name = db.Column(db.String, nullable=True)
    surname = db.Column(db.String, index=True, nullable=True)
    middle_name = db.Column(db.String, nullable=True)
    role_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("roles.id"), index=True,
                                nullable=True)
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
        return check_password_hash(self.hashed_password, password)

    @property
    def full_name(self):
        return f"{self.surname} {self.name} {self.middle_name}"

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    @singledispatchmethod
    def has_role(self, role: str):
        return self.role.name == role

    @has_role.register
    def _(self, role: int):
        return self.role_id == role

    def __repr__(self):
        return '<User %r>' % "; ".join(map(str, [self.id, self.login, self.surname, self.role_id]))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


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
    is_free = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
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

