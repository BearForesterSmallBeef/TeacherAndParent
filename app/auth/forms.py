from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired


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