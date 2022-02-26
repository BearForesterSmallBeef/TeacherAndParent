from flask import Blueprint, redirect, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

auth = Blueprint("auth", __name__)


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


@auth.route("/signup", methods=["GET", 'POST'])
def signup_user_status():
    register_form = RegisterTypeForm()
    if register_form.validate_on_submit():
        user_status = register_form.user_status.data
        return redirect(f"/signup/{user_status}")
    return render_template("auth/register.html", form=register_form,
                           header="Регистрация. Тип пользователя.")


@auth.route("/signup/parent", methods=["GET", "POST"])
def register_parent():
    register_form = RegisterParentForm()
    if register_form.validate_on_submit():
        return redirect("/login")
    return render_template("auth/register.html", form=register_form,
                           header="Регистрация. Родитель.")


@auth.route("/signup/teacher", methods=["GET", "POST"])
def register_teacher():
    register_form = RegisterTeacherForm()
    if register_form.validate_on_submit():
        return redirect("/login")
    return render_template("auth/register.html", form=register_form,
                           header="Регистрация. Учитель.")