from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, PasswordField, BooleanField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, InputRequired

#from flask import (Blueprint, redirect, render_template, request, flash, url_for,
#                   abort)
#from flask_login import login_user, login_required, logout_user, current_user
#
#from app import db
#from app.models import Class, User, Parent, RolesIds, Permissions, Subject
#from .utils import permissions_accepted, permissions_required


class MultiCheckboxField(SelectMultipleField):
  widget = widgets.ListWidget(prefix_label=False)
  option_widget = widgets.CheckboxInput()


class RegisterTypeForm(FlaskForm):
    user_status = SelectField("Статус", choices=[("parent", "Родитель"), ("teacher", "Учитель")])
    submit = SubmitField("Далее")


class RegisterParentForm(FlaskForm):
    full_name = StringField("ФИО", validators=[DataRequired()])
    school = StringField("Школа", validators=[DataRequired()])
    submit = SubmitField("Зарегистрироваться")


class RegisterTeacherForm(FlaskForm):
    full_name = StringField("ФИО", validators=[DataRequired()])
    forms = SelectField("Классы", choices=list(zip(map(lambda x: f"form{x}", range(1, 12)),
                                                   range(1, 12))))
    subjects = SelectField("Предметы", choices=[("math", "Математика"), ("physics", "Физика"),
                                                ("it", "Информатика")])
    submit = SubmitField("Зарегистрироваться")


class RegistrationParentForm(FlaskForm):
    login = StringField('Логин', validators=[InputRequired()])
    username = StringField('Имя', validators=[InputRequired()])
    usersurename = StringField('Фамилия', validators=[InputRequired()])
    usermiddlename = StringField('Отчество', validators=[InputRequired()])
    password = StringField('Пароль', validators=[InputRequired()])
    classes = SelectField("Класс", validate_choice=False)
    submit = SubmitField('Создать новую учетную запись родителя')


class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[InputRequired()])
    password = PasswordField('Пароль', validators=[InputRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class DeleteUser(FlaskForm):
    login = StringField('Логин удаляемой учетной записи', validators=[InputRequired()])
    password = PasswordField('Пароль удаляемой учетной записи', validators=[InputRequired()])
    delete = BooleanField('Я уверен, что хочу удалиить эту запись')
    submit = SubmitField('Удалить')
