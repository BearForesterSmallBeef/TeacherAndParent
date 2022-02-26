from flask import Blueprint, redirect, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DecimalRangeField, SubmitField
from wtforms.validators import DataRequired, NumberRange

auth = Blueprint("auth", __name__)


class RegisterForm(FlaskForm):
    full_name = StringField("ФИО", validators=[DataRequired()])
    school = StringField("Школа", validators=[DataRequired()])
    status = SelectField("Статус", choices=[("parent", "Родитель"), ("teacher", "Учитель")],
                         default="parent")
    forms = SelectField("Классы", choices=list(zip(map(lambda x: f"form{x}", range(1, 12)),
                                                   range(1, 12))))
    subjects = SelectField("Предметы", choices=[("math", "Математика"), ("physics", "Физика"),
                                                ("it", "Информатика")])
    submit = SubmitField("Зарегистрироваться")


@auth.route("/signup", methods=["GET", 'POST'])
def signup():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        return redirect("/login")
    return render_template("auth/register.html", form=register_form)