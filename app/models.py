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
    login = db.Column(db.String, index=True, unique=True, nullable=True)
    hashed_password = db.Column(db.String, index=True, nullable=True)
    name = db.Column(db.String, nullable=True)
    surname = db.Column(db.String, index=True, nullable=True)
    middle_name = db.Column(db.String, nullable=True)
    role_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("roles.id"), index=True, nullable=True)
    role = orm.relation('Role')
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now, nullable=True)

    def __repr__(self):
        return '<User %r>' % "; ".join(map(str, [self.id, self.login, self.surname, self.role_id]))

    def get_hash(self, password):
        from werkzeug.security import generate_password_hash

        return generate_password_hash(password)

    def check_hash(self, hash, password):
        from werkzeug.security import check_password_hash

        return check_password_hash(hash, password)


class Parent(db.Model):
    __tablename__ = 'parents'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    parent_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), index=True)
    parent = orm.relation('User')
    class_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("classes.id"), index=True)
    Class = orm.relation('Class')

    def __repr__(self):
        return '<Parent %r>' % "; ".join(map(str, [self.parent_id, self.class_id]))


class TeacherObjectsClasses(db.Model):
    __tablename__ = 'teacher_objects_classes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    teacher_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), index=True)
    teacher = orm.relation('User')
    object_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("objects.id"), index=True)
    object = orm.relation('Object')
    class_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("classes.id"), index=True)
    Class = orm.relation('Class')

    def __repr__(self):
        return '<TeacherObjectsClasses %r>' % "; ".join(map(str, [self.id, self.teacher_id, self.object_id,
                                                                             self.class_id]))


class Consultation(db.Model):
    __tablename__ = 'consultations'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    teacher_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), index=True)
    teacher = orm.relation(User, foreign_keys=teacher_id)
    parent_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), index=True)
    parent = orm.relationship(User, foreign_keys=parent_id)
    consultation_start_time = sqlalchemy.Column(sqlalchemy.DateTime)
    consultation_finish_time = sqlalchemy.Column(sqlalchemy.DateTime)
    status = sqlalchemy.Column(sqlalchemy.Boolean, default=True)

    def __repr__(self):
        return '<Consultation %r>' % "; ".join(map(str, [self.id, self.teacher_id, self.parent_id, self.status,
                                                         self.consultation_start_time, self.consultation_finish_time]))


# TODO разобраться с миграциями +
# TODO заполнение тестовами данными
# TODO Формочка для админа
# TODO разобраться c login`ами и role`ами
