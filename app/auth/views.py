from flask import Blueprint, redirect, render_template, request

from .forms import RegisterTypeForm, RegisterParentForm, RegisterTeacherForm, RegistrationParentForm, LoginForm
from app import db
from app.models import Class, User, Parent, Consultation, TeacherSubjectsClasses, Subject, RolesIds


auth = Blueprint("auth", __name__)


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


def create_parent(login, password, name, surname, classes,  middle_name=""):
    try:
        db.session.add(
            User(login=login, password=password,
                 name=name,
                 surname=surname, middle_name=middle_name,
                 role_id=RolesIds.PARENT))
        user_id = db.session.query(User).filter(User.login == login).first().id
        class_id = db.session.query(Class).filter(Class.name == classes).first().id
        db.session.add(
            Parent(user_id=user_id, class_id=class_id))
        db.session.commit()
    except Exception as ex:
        print(ex)
        return 0
    return 1


@auth.route("/parent_registration", methods=['GET', 'POST'])
def parent_registration():
    form = RegistrationParentForm()
    form.classes.choices = sorted([(i.name, i.name) for i in db.session.query(Class)],
                                  key=lambda x: int(x[0].split("-")[0]))
    if form.validate_on_submit():
        flag = create_parent(request.form["login"], request.form["password"], request.form["username"],
                             request.form["usersurename"], request.form["classes"],
                             middle_name=str(request.form["usermiddlename"]))
        return redirect(f"/reg_result/{flag}")
    return render_template("auth/auth.html", form=form)


@auth.route("/reg_result/<ok>", methods=['GET', 'POST'])
def reg_result(ok):
    flag = bool(int(ok))
    if request.form.get('Назад') == 'Назад':
        return redirect('/parent_registration')
    return render_template("auth/reg_result.html", flag=flag)


@auth.route("/user_login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    text = "Вход в учетную запись"
    return render_template("auth/auth.html", form=form, header=text)
