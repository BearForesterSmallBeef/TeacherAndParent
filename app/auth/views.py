from flask import Blueprint, redirect, render_template, request, flash

from app import db
from app.models import Class, User, Parent, RolesIds
from .forms import (RegisterTypeForm, RegisterParentForm, RegisterTeacherForm,
                    RegistrationParentForm, LoginForm)

auth = Blueprint("auth", __name__)


@auth.route("/signup", methods=["GET", 'POST'])
def signup_user_status():
    register_form = RegisterTypeForm()
    if register_form.validate_on_submit():
        user_status = register_form.user_status.data
        return redirect(f"/signup/{user_status}")
    return render_template("auth/register.html", form=register_form,
                           header="Регистрация. Тип пользователя.")


def create_parent(login, password, name, surname, classes, middle_name=""):
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


@auth.route("/signup/parent", methods=['GET', 'POST'])
def parent_registration():
    form = RegistrationParentForm()
    form.classes.choices = sorted([(i.name, i.name) for i in db.session.query(Class)],
                                  key=lambda x: int(x[0].split("-")[0]))
    if form.validate_on_submit():
        flag = create_parent(request.form["login"], request.form["password"],
                             request.form["username"],
                             request.form["usersurename"], request.form["classes"],
                             middle_name=str(request.form["usermiddlename"]))
        flag = bool(int(flag))
        if flag:
            flash("Учетная запись для родителя успешна создана", category="success")
        else:
            flash("ПРОИЗОШЕЛ СБОЙ, пожалуйста, повторите попытку позже", category="error")
        return redirect(f"/")
    return render_template("auth/auth.html", form=form)


@auth.route("/signup/parent/reg_result/<ok>", methods=['GET', 'POST'])
def reg_result(ok):
    flag = bool(int(ok))
    if request.form.get('Назад') == 'Назад':
        return redirect('/signup/parent')
    return render_template("auth/reg_result.html", flag=flag)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    text = "Вход в учетную запись"
    return render_template("auth/auth.html", form=form, header=text)
