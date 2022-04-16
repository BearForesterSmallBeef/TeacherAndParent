from flask import (Blueprint, redirect, render_template, request, flash, url_for,
                   abort)
from flask_login import login_user, login_required, logout_user, current_user

from app import db
from app.models import Class, User, Parent, RolesIds, Permissions, Subject
from .forms import RegisterTypeForm, RegistrationParentForm, LoginForm
from .utils import permissions_accepted, permissions_required

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, PasswordField, BooleanField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, InputRequired

auth = Blueprint("auth", __name__)


@auth.route("/signup")
@permissions_accepted(Permissions.CREATE_PARENTS, Permissions.CREATE_TEACHERS)
def signup():
    if (current_user.can(Permissions.CREATE_PARENTS) and
            current_user.can(Permissions.CREATE_TEACHERS)):
        return redirect(url_for(".head_choose_signup_type"))
    elif current_user.can(Permissions.CREATE_PARENTS):
        return redirect(url_for(".parent_registration"))
    else:
        abort(403)


@auth.route("/signup/head_choose", methods=["GET", 'POST'])
@permissions_required(Permissions.CREATE_PARENTS, Permissions.CREATE_TEACHERS)
def head_choose_signup_type():
    register_form = RegisterTypeForm()
    if register_form.validate_on_submit():
        user_status = register_form.user_status.data
        return redirect(f"/signup/{user_status}")
    return render_template("auth/register.html", form=register_form,
                           header="Регистрация. Тип пользователя.")


def create_parent(login, password, name, surname, classes, middle_name=""):
    try:
        parallel = classes[:classes.find("-")]
        groups = classes[classes.find("-") + 1:]
        db.session.add(
            User(login=login, password=password,
                 name=name,
                 surname=surname, middle_name=middle_name,
                 role_id=RolesIds.PARENT))
        user_id = db.session.query(User).filter(User.login == login).first().id
        class_id = db.session.query(Class).filter(Class.parallel == parallel and Class.groups == groups).first().id
        db.session.add(
            Parent(user_id=user_id, class_id=class_id))
        db.session.commit()
    except Exception as ex:
        print(ex)
        return 0
    return 1


@auth.route("/signup/parent", methods=['GET', 'POST'])
@permissions_required(Permissions.CREATE_PARENTS)
def parent_registration():
    form = RegistrationParentForm()
    form.classes.choices = sorted([(str(i.parallel) + "-" + i.groups, str(i.parallel) + "-" + i.groups)
                                   for i in db.session.query(Class)],
                                  key=lambda x: (int(x[0].split("-")[0]), x[0].split("-")[1]))
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
        return redirect(f"/signup")
    return render_template("auth/auth.html", form=form)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data.lower()).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash("Вы успешно авторизовались.", category="success")
            nxt = request.args.get('next')
            if nxt is None or not nxt.startswith('/'):
                nxt = url_for('main.index')
            return redirect(nxt)
        flash('Неверный логин или пароль.', category="error")
    text = "Вход в учетную запись"
    return render_template("auth/auth.html", form=form, header=text)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы успешно вышли из аккаунта', category="success")
    return redirect(url_for('main.index'))


@auth.route('/signup/teacher', methods=['GET', 'POST'])
def teacher_registration():

    class MultiCheckboxField(SelectMultipleField):
        widget = widgets.TableWidget()
        option_widget = widgets.CheckboxInput()

    class RegistrationTeacherForm(FlaskForm):
        cl = sorted(db.session.query(Class), key=lambda x: (x.parallel, x.groups))
        classes = [(i.id, str(i.parallel) + "-" + i.groups) for i in cl]
        parallels = set([i.parallel for i in cl])
        objects = [i.name for i in db.session.query(Subject)]
        for i in objects:
            for j in parallels:
                print(j)
                lambda x: int(x[1].splite("-")[0]) == j
                locals()[i + str(j)] = MultiCheckboxField("",
                                                          choices=list(filter(lambda x:
                                                                              int(x[1].splite("-")[0]) == i, classes)),
                                                          coerce=int)

    form = RegistrationTeacherForm()
    subjects = list(db.session.query(Subject))
    classes = list(db.session.query(Class))
    print(form["ОБЖ"])
    if form.validate_on_submit():
        return "чикибамбони"
    else:
        return render_template("auth/techer_auth.html", form=form, subjects=subjects)
