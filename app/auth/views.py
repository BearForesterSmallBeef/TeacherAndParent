from flask import (Blueprint, redirect, render_template, request, flash, url_for,
                   abort)
from flask_login import login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from sqlalchemy import null
from wtforms import StringField, SubmitField, SelectMultipleField, widgets
from wtforms.validators import InputRequired

from app import db
from app.models import Class, User, Parent, RolesIds, Permissions, Subject, TeacherSubjectsClasses, \
    Consultation
from .forms import RegisterTypeForm, RegistrationParentForm, LoginForm, DeleteUser, AddSubject, AddClass, AddTypeForm
from .utils import permissions_accepted, permissions_required

auth = Blueprint("auth", __name__)


@auth.route("/signup")
@permissions_accepted(Permissions.MANAGE_PARENTS, Permissions.MANAGE_TEACHERS)
def signup():
    if (current_user.can(Permissions.MANAGE_PARENTS) and
            current_user.can(Permissions.MANAGE_TEACHERS)):
        return redirect(url_for(".head_choose_signup_type"))
    elif current_user.can(Permissions.MANAGE_PARENTS):
        return redirect(url_for(".parent_registration"))
    else:
        abort(403)


@auth.route("/add")
@permissions_accepted(Permissions.CREATE_TEACHERS)
def add():
    if current_user.can(Permissions.CREATE_TEACHERS):
        return redirect(url_for(".head_choose_add_type"))
    else:
        abort(403)


@auth.route("/delete")
@permissions_accepted(Permissions.MANAGE_PARENTS, Permissions.MANAGE_TEACHERS)
def delete():
    if (current_user.can(Permissions.MANAGE_PARENTS) and
            current_user.can(Permissions.MANAGE_TEACHERS)):
        return redirect(url_for(".head_choose_delete_type"))
    elif current_user.can(Permissions.MANAGE_PARENTS):
        return redirect(url_for(".delete_parent"))
    else:
        abort(403)


@auth.route("/delete/head_choose", methods=["GET", 'POST'])
@permissions_required(Permissions.MANAGE_PARENTS, Permissions.MANAGE_TEACHERS)
def head_choose_delete_type():
    register_form = RegisterTypeForm()
    if register_form.validate_on_submit():
        user_status = register_form.user_status.data
        return redirect(f"/delete/{user_status}")
    return render_template("auth/register.html", form=register_form,
                           header="Удаление. Тип пользователя.")


@auth.route("/signup/head_choose", methods=["GET", 'POST'])
@permissions_required(Permissions.MANAGE_PARENTS, Permissions.MANAGE_TEACHERS)
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
        class_id = db.session.query(Class).filter(
            Class.parallel == parallel and Class.groups == groups).first().id
        db.session.add(
            Parent(user_id=user_id, class_id=class_id))
        db.session.commit()
    except Exception as ex:
        print(ex)
        return 0
    return 1


@auth.route("/signup/parent", methods=['GET', 'POST'])
@permissions_required(Permissions.MANAGE_PARENTS)
def parent_registration():
    form = RegistrationParentForm()
    form.classes.choices = sorted(
        [(str(i.parallel) + "-" + i.groups, str(i.parallel) + "-" + i.groups)
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


def create_teacher(login, password, name, surname, class_dict=dict(), middle_name=""):
    try:
        db.session.add(
            User(login=login, password=password,
                 name=name,
                 surname=surname, middle_name=middle_name,
                 role_id=RolesIds.TEACHER))
        self_id = db.session.query(User).filter(User.login == login).first().id
        for i in class_dict.keys():
            subject_id = db.session.query(Subject).filter(Subject.name == i).first().id
            for j in class_dict[i]:
                db.session.add(TeacherSubjectsClasses(teacher_id=self_id, subject_id=subject_id,
                                                      class_id=int(j)))
        db.session.commit()
    except Exception as ex:
        print(ex)
        return 0
    return 1


@auth.route('/signup/teacher', methods=['GET', 'POST'])
@permissions_required(Permissions.MANAGE_TEACHERS)
def teacher_registration():
    class MultiCheckboxField(SelectMultipleField):
        widget = widgets.TableWidget()
        option_widget = widgets.CheckboxInput()

    class RegistrationTeacherForm(FlaskForm):
        login = StringField('Логин', validators=[InputRequired()])
        username = StringField('Имя', validators=[InputRequired()])
        usersurename = StringField('Фамилия', validators=[InputRequired()])
        usermiddlename = StringField('Отчество', validators=[InputRequired()])
        password = StringField('Пароль', validators=[InputRequired()])

        # creating tables with subjects
        cl = sorted(db.session.query(Class), key=lambda x: (x.parallel, x.groups))
        classes = [(i.id, str(i.parallel) + "-" + i.groups) for i in cl]
        parallels = set([i.parallel for i in cl])

        subjects = [i.name for i in db.session.query(Subject)]

        classes_parallels = {}
        for j in parallels:
            classes_parallels[j] = [(i.id, str(i.parallel) + "-" + i.groups)
                                    for i in db.session.query(Class).filter(Class.parallel == j)]

        for i in classes_parallels.keys():
            classes_parallels[i].sort(key=lambda x: x[1].split("-")[1:])

        for i in subjects:
            for j in classes_parallels.keys():
                locals()[i + str(j)] = MultiCheckboxField("", choices=classes_parallels[j],
                                                          coerce=int)
        # end of creating
        submit = SubmitField('Создать новую учетную запись учителя')

    form = RegistrationTeacherForm()
    subjects = list(db.session.query(Subject))
    classes = list(db.session.query(Class))

    parallels = list(set([i.parallel for i in db.session.query(Class)]))
    parallels.sort()
    parallels = list(map(str, parallels))

    if form.is_submitted() and form.validate():
        formlist = list(request.form)
        class_dict = {}
        for i in subjects:
            for j in parallels:
                if (i.name + str(j)) in formlist:
                    if i.name not in class_dict.keys():
                        class_dict[i.name] = []
                    class_dict[i.name] += form.data[i.name + str(j)]
                    class_dict[i.name] = list(set(class_dict[i.name]))
        flag = create_teacher(form.data["login"], form.data["password"], form.data["username"],
                              form.data["usersurename"], middle_name=form.data["usermiddlename"],
                              class_dict=class_dict)
        if flag:
            flash("Учетная запись для учителя успешна создана", category="success")
        else:
            flash("ПРОИЗОШЕЛ СБОЙ, пожалуйста, повторите попытку позже", category="error")
        return redirect(f"/signup")
    else:
        return render_template("auth/techer_auth.html", form=form, subjects=subjects,
                               parallels=parallels)


def delete_user(login, password, role=-1):
    try:
        user = db.session.query(User).filter(User.login == login).first()
        if not user:
            return 2
        if user.role_id != role and role != -1:
            return 2
        if not user.verify_password(password):
            return 2
        self_id = user.id
        db.session.delete(user)
        if role == RolesIds.TEACHER:
            tcs = db.session.query(TeacherSubjectsClasses).filter(
                TeacherSubjectsClasses.teacher_id == self_id)
            cons = db.session.query(Consultation).filter(Consultation.teacher_id == self_id)
            for i in tcs:
                db.session.delete(i)
            for i in cons:
                db.session.delete(i)
        if role == RolesIds.PARENT:
            pars = db.session.query(Parent).filter(Parent.user_id == self_id)
            for i in pars:
                db.session.delete(i)
            cons = db.session.query(Consultation).filter(Consultation.parent_id == self_id)
            for i in cons:
                i.parent_id = null()
                i.is_free = 1
        db.session.commit()
    except Exception as ex:
        print(ex)
        return 0
    return 1


@auth.route('/delete/teacher', methods=['GET', 'POST'])
@permissions_required(Permissions.MANAGE_TEACHERS)
def delete_teacher():
    form = DeleteUser()
    if form.validate_on_submit() and form.data["delete"]:
        flag = delete_user(form.data["login"], form.data["password"], role=RolesIds.TEACHER)
        if flag == 1:
            flash("Учетная запись учителя успешна удалена", category="success")
        elif flag == 0:
            flash("ПРОИЗОШЕЛ СБОЙ, пожалуйста, повторите попытку позже", category="error")
        elif flag == 2:
            flash("Некоректный ввод данных", category="error")
        return redirect(f"/delete")
    return render_template("auth/auth.html", form=form, header="Удаление учетной записи учителя")


@auth.route('/delete/parent', methods=['GET', 'POST'])
@permissions_required(Permissions.MANAGE_PARENTS)
def delete_parent():
    form = DeleteUser()
    if form.validate_on_submit() and form.data["delete"]:
        flag = delete_user(form.data["login"], form.data["password"], role=RolesIds.PARENT)
        if flag == 1:
            flash("Учетная запись родителя успешна удалена", category="success")
        elif flag == 0:
            flash("ПРОИЗОШЕЛ СБОЙ, пожалуйста, повторите попытку позже", category="error")
        elif flag == 2:
            flash("Некоректный ввод данных", category="error")
        return redirect(f"/delete")
    return render_template("auth/auth.html", form=form, header="Удаление учетной записи родителя")


@auth.route("/add/head_choose", methods=["GET", 'POST'])
@permissions_required(Permissions.CREATE_TEACHERS)
def head_choose_add_type():
    register_form = AddTypeForm()
    if register_form.validate_on_submit():
        adding = register_form.user_status.data
        return redirect(f"/add/{adding}")
    return render_template("auth/register.html", form=register_form,
                           header="Добавление. Тип объекта.")


def create_subject(name, about):
    try:
        db.session.add(
            Subject(name=name, about=about)
        )
        db.session.commit()
    except Exception as ex:
        print(ex)
        return 0
    return 1


@auth.route('/add/subject', methods=['GET', 'POST'])
@permissions_required(Permissions.CREATE_TEACHERS)
def add_subject():
    form = AddSubject()
    if form.validate_on_submit():
        flag = create_subject(form.data["name"], form.data["about"])
        if flag == 1:
            flash("Предмет успешно создан", category="success")
        elif flag == 0:
            flash("ПРОИЗОШЕЛ СБОЙ, пожалуйста, повторите попытку позже", category="error")
        return redirect(f"/add")
    else:
        return render_template("auth/auth.html", form=form, header="Добавление предмета")


def create_class(about, parallel, groups):
    try:
        db.session.add(
            Class(about=about, parallel=int(parallel), groups=groups)
        )
        db.session.commit()
    except Exception as ex:
        print(ex)
        return 0
    return 1


@auth.route('/add/class', methods=['GET', 'POST'])
@permissions_required(Permissions.CREATE_TEACHERS)
def add_class():
    form = AddClass()
    if form.validate_on_submit():
        flag = create_class(form.data["about"], form.data["parallel"], form.data["groups"])
        if flag == 1:
            flash("Класс успешно создан", category="success")
        elif flag == 0:
            flash("ПРОИЗОШЕЛ СБОЙ, пожалуйста, повторите попытку позже", category="error")
        return redirect(f"/add")
    else:
        return render_template("auth/auth.html", form=form, header="Добавление класса")
