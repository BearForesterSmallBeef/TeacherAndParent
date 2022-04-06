from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, InputRequired


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

