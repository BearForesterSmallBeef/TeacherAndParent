from flask import (Blueprint, redirect, render_template, request, flash, url_for,
                   abort)
from flask_login import login_user, login_required, logout_user, current_user

from app import db
from app.models import Class, User, Parent, RolesIds, Permissions
from .forms import RegisterTypeForm, RegistrationParentForm, LoginForm
from .utils import permissions_accepted, permissions_required

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
@permissions_required(Permissions.CREATE_PARENTS)
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
