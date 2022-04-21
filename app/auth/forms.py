from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, PasswordField, BooleanField, \
    SelectMultipleField, widgets, DateField, DateTimeField
from wtforms.validators import DataRequired, InputRequired, URL, ValidationError, length

from app.models import User


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class RegisterTypeForm(FlaskForm):
    user_status = SelectField("Статус", choices=[])
    submit = SubmitField("Далее")


class AddTypeForm(FlaskForm):
    user_status = SelectField("Объект", choices=[("subject", "Предмет"), ("class", "Класс")])
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
    login = StringField('Логин', validators=[InputRequired(), length(min=10)])
    username = StringField('Имя', validators=[InputRequired(), length(min=10)])
    usersurename = StringField('Фамилия', validators=[InputRequired()])
    usermiddlename = StringField('Отчество', validators=[InputRequired()])
    password = StringField('Пароль', validators=[InputRequired()])
    classes = SelectField("Класс", validate_choice=False)
    submit = SubmitField('Создать новую учетную запись родителя')


class RegistrationHeadTeacherForm(FlaskForm):
    login = StringField('Логин', validators=[InputRequired(), length(min=10)])
    username = StringField('Имя', validators=[InputRequired(), length(min=10)])
    usersurename = StringField('Фамилия', validators=[InputRequired()])
    usermiddlename = StringField('Отчество', validators=[InputRequired()])
    password = StringField('Пароль', validators=[InputRequired()])
    submit = SubmitField('Создать')


class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[InputRequired()])
    password = PasswordField('Пароль', validators=[InputRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class DeleteUser(FlaskForm):
    login = StringField('Логин удаляемой учетной записи', validators=[InputRequired()])
    password = PasswordField('Пароль удаляемой учетной записи', validators=[InputRequired()])
    delete = BooleanField('Я уверен, что хочу удалить эту запись')
    submit = SubmitField('Удалить')


class AddSubject(FlaskForm):
    name = StringField('Название', validators=[InputRequired()])
    about = StringField('Описание', validators=[InputRequired()], default="Это новый предмет!")
    submit = SubmitField('Добавить')


class AddClass(FlaskForm):
    parallel = SelectField("Параллель", choices=[(i, i) for i in range(1, 12)])
    groups = StringField('Группы', validators=[InputRequired()])
    about = StringField('Описание', validators=[InputRequired()], default="Это новый класс!")
    submit = SubmitField('Добавить')


class ManageConsultationForm(FlaskForm):
    parent_login = StringField('Логин родителя')

    def validate_parent_login(self, field):
        exists = User.query.filter_by(login=field.data).first() is not None
        if not exists:
            raise ValidationError("Такого пользователя не существует")
        if self.is_free.data:
            raise ValidationError("Если указан родитель, то консультация должна быть занянта")

    date = DateField("Дата", validators=[InputRequired()])
    start_time = DateTimeField("Начало", validators=[InputRequired()], format="%H:%M",
                               render_kw={"placeholder": "13:10"})
    duration = SelectField("Продолжительность", validators=[InputRequired()],
                           choices=range(5, 61, 5))
    is_free = BooleanField("Свободна ли")

    def validate_is_free(self, field):
        if field.data and not self.parent_login.data:
            raise ValidationError("Если консультация не свободна, то укажите родителя")

    url = StringField("Ссылка", validators=[URL()])

    submit = SubmitField('Добавить')


class Agree(FlaskForm):
    agree = BooleanField("Подтверждение действия")
    submit = SubmitField('Продолжить')


class HardAgree(FlaskForm):
    login = StringField('Логин', validators=[InputRequired()])
    password = PasswordField('Пароль', validators=[InputRequired()])
    agree = BooleanField("Подтверждение действия")
    submit = SubmitField('Продолжить')
