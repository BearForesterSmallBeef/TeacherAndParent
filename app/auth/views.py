import datetime
import os
import random

from excel.excel_funcs import data_parent_registration
from flask import (Blueprint, redirect, render_template, request, flash, url_for)
from flask_login import login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from sqlalchemy import null
from wtforms import StringField, SubmitField, SelectMultipleField, widgets
from wtforms.validators import InputRequired
from werkzeug.utils import secure_filename, send_from_directory
from app import db
from app.models import Class, User, Parent, RolesIds, Permissions, Subject, TeacherSubjectsClasses, \
    Consultation, Role
from .forms import RegisterTypeForm, RegistrationParentForm, LoginForm, DeleteUser, AddSubject, \
    AddClass, AddTypeForm, RegistrationHeadTeacherForm, ManageConsultationForm, Agree, GetResult
from .utils import permissions_accepted, permissions_required
from excel.excel_funcs import ExcelErrors

auth = Blueprint("auth", __name__)
UPLOAD_FOLDER = 'excel\\files'


def create_reg(length=10, check_login=True):
    chars = "0123456789qwertyuiopasdfghjkzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
    reg = ""
    for i in range(length):
        reg += chars[random.randrange(0, len(chars))]
    if check_login:
        iteration = 0
        while not db.session.query(User).filter(User.login == reg):
            iteration += 1
            for i in range(length):
                reg += chars[random.randrange(0, len(chars))]
            if iteration == 20:
                iteration = 0
                length += 1
    return reg


def get_registration_type_form():
    register_form = RegisterTypeForm()
    user_statuses = []
    if current_user.can(Permissions.MANAGE_PARENTS):
        user_status = Role.query.get(RolesIds.PARENT).name
        user_status = (user_status, "Родитель")
        user_statuses.append(user_status)
    if current_user.can(Permissions.MANAGE_TEACHERS):
        user_status = Role.query.get(RolesIds.TEACHER).name
        user_status = (user_status, "Учитель")
        user_statuses.append(user_status)
    if current_user.can(Permissions.MANAGE_HEAD_TEACHER):
        user_status = Role.query.get(RolesIds.HEAD_TEACHER).name
        user_status = (user_status, "Завуч")
        user_statuses.append(user_status)
    register_form.user_status.choices = user_statuses
    return register_form


@auth.route("/signup")
@permissions_accepted(Permissions.MANAGE_PARENTS,
                      Permissions.MANAGE_TEACHERS,
                      Permissions.MANAGE_HEAD_TEACHER)
def signup():
    return redirect(url_for(".choose_signup_type"))


@auth.route("/add")
@permissions_accepted(Permissions.MANAGE_OBJECTS)
def add():
    return redirect(url_for(".choose_add_type"))


@auth.route("/delete")
@permissions_accepted(Permissions.MANAGE_PARENTS,
                      Permissions.MANAGE_TEACHERS,
                      Permissions.MANAGE_HEAD_TEACHER)
def delete():
    return redirect(url_for(".choose_delete_type"))


@auth.route("/delete/choose", methods=["GET", 'POST'])
@permissions_accepted(Permissions.MANAGE_PARENTS,
                      Permissions.MANAGE_TEACHERS,
                      Permissions.MANAGE_HEAD_TEACHER)
def choose_delete_type():
    register_form = get_registration_type_form()
    user_statuses = register_form.user_status.choices
    if len(user_statuses) == 1:  # если может создавать только одного типа пользователя,
        # то сразу перенаправляем на нужную страницу
        user_status_slug = user_statuses[0][0]
        return redirect(f"/delete/{user_status_slug}")
    if register_form.validate_on_submit():
        user_status = register_form.user_status.data
        return redirect(f"/delete/{user_status}")
    return render_template("auth/auth.html", form=register_form,
                           header="Удаление. Тип пользователя.")


@auth.route("/signup/choose", methods=["GET", 'POST'])
@permissions_accepted(Permissions.MANAGE_PARENTS,
                      Permissions.MANAGE_TEACHERS,
                      Permissions.MANAGE_HEAD_TEACHER)
def choose_signup_type():
    register_form = get_registration_type_form()
    user_statuses = register_form.user_status.choices
    if len(user_statuses) == 1:  # если может создавать только одного типа пользователя,
        # то сразу перенаправляем на нужную страницу
        user_status_slug = user_statuses[0][0]
        return redirect(f"/signup/{user_status_slug}")
    if register_form.validate_on_submit():
        user_status = register_form.user_status.data
        return redirect(f"/signup/{user_status}")
    return render_template("auth/auth.html", form=register_form,
                           header="Регистрация. Тип пользователя.")


def create_parent(login, password, name, surname, classes, middle_name=""):
    try:
        if len(login) < 10 or len(password) < 10:
            return 8
        if db.session.query(User).filter(User.login == login).first():
            return 11
        try:
            parallel = classes[:classes.find("-")]
            groups = classes[classes.find("-") + 1:]
            class_id = db.session.query(Class).filter(
                Class.parallel == parallel and Class.groups == groups).first().id
        except Exception as ex:
            print(ex)
            return 6
        db.session.add(
            User(login=login, password=password,
                 name=name,
                 surname=surname, middle_name=middle_name,
                 role_id=RolesIds.PARENT))
        user_id = db.session.query(User).filter(User.login == login).first().id
        db.session.add(
            Parent(user_id=user_id, class_id=class_id))
        db.session.commit()
    except Exception as ex:
        print(ex)
        return 8
    return 0


@auth.route("/signup/parent", methods=['GET', 'POST'])
@permissions_required(Permissions.MANAGE_PARENTS)
def parent_registration():
    form = RegistrationParentForm()
    form.login.data = create_reg()
    form.password.data = create_reg(check_login=False)
    form.classes.choices = sorted(
        [(str(i.parallel) + "-" + i.groups, str(i.parallel) + "-" + i.groups)
         for i in db.session.query(Class)],
        key=lambda x: (int(x[0].split("-")[0]), x[0].split("-")[1]))
    if form.validate_on_submit():
        flag = create_parent(request.form["login"], request.form["password"],
                             request.form["username"],
                             request.form["usersurename"], request.form["classes"],
                             middle_name=str(request.form["usermiddlename"]))
        flag = bool(int(flag == 0))
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
        user = User.query.filter_by(login=form.login.data).first()
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


def create_teacher(login, password, name, surname, class_dict=None, middle_name=""):
    if class_dict is None:
        class_dict = {}
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


@auth.route("/signup/head_teacher", methods=['GET', 'POST'])
@permissions_required(Permissions.MANAGE_HEAD_TEACHER)
def head_teacher_registration():
    form = RegistrationHeadTeacherForm()
    if form.validate_on_submit():
        try:
            head_teacher = User(login=form.login.data,
                                password=form.password.data,
                                name=form.username.data,
                                surname=form.usersurename.data,
                                middle_name=form.usermiddlename.data,
                                role_id=RolesIds.HEAD_TEACHER)
        except Exception as e:
            flag = 0
            print(e)
        else:
            flag = 1
            db.session.add(head_teacher)
            db.session.commit()
        if flag:
            flash("Учетная запись для завуча успешна создана", category="success")
        else:
            flash("ПРОИЗОШЕЛ СБОЙ, пожалуйста, повторите попытку позже", category="error")
        return redirect(f"/signup")
    return render_template("auth/auth.html", form=form, header="Создание учетной записи завуча")


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


@auth.route('/delete/head_teacher', methods=['GET', 'POST'])
@permissions_required(Permissions.MANAGE_PARENTS)
def delete_head_teacher():
    form = DeleteUser()
    if form.validate_on_submit() and form.data["delete"]:
        flag = delete_user(form.data["login"], form.data["password"], role=RolesIds.PARENT)
        if flag == 1:
            flash("Учетная запись завуча успешна удалена", category="success")
        elif flag == 0:
            flash("ПРОИЗОШЕЛ СБОЙ, пожалуйста, повторите попытку позже", category="error")
        elif flag == 2:
            flash("Некоректный ввод данных", category="error")
        return redirect(f"/delete")
    return render_template("auth/auth.html", form=form, header="Удаление учетной записи завуча")


@auth.route("/add/choose", methods=["GET", 'POST'])
@permissions_required(Permissions.MANAGE_OBJECTS)
def choose_add_type():
    register_form = AddTypeForm()
    if register_form.validate_on_submit():
        adding = register_form.user_status.data
        return redirect(f"/add/{adding}")
    return render_template("auth/auth.html", form=register_form,
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
@permissions_required(Permissions.MANAGE_OBJECTS)
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
@permissions_required(Permissions.MANAGE_OBJECTS)
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


@auth.route("/teacher/consultations/create", methods=["GET", "POST"])
@permissions_required(Permissions.MANAGE_CONSULTATIONS)
def create_consultation():
    form = ManageConsultationForm()
    if form.validate_on_submit():
        parent = User.query.filter_by(login=form.parent_login.data).first()
        start_time = form.start_time.data
        duration = int(form.duration.data)
        finish_time = (start_time + datetime.timedelta(minutes=duration)).time()
        consultation = Consultation(teacher_id=current_user.id, parent_id=getattr(parent, "id"),
                                    date=form.date.data, start_time=start_time.time(),
                                    finish_time=finish_time, is_free=form.is_free.data,
                                    url=form.url.data)
        db.session.add(consultation)
        db.session.commit()
        return redirect(url_for("main.teacher_consultations"))
    return render_template("teacher/manage_consultation.html", form=form,
                           header="Создать консультацию")


@auth.route("/teacher/consultations/edit/<int:consultation_id>", methods=["GET", "POST"])
@permissions_required(Permissions.MANAGE_CONSULTATIONS)
def edit_consultation(consultation_id):
    form = ManageConsultationForm()
    consultation = Consultation.query.get(consultation_id)
    if consultation is None:
        flash("Консультация не найдена", category="error")
        return redirect(url_for("main.teacher_consultations"))
    if form.validate_on_submit():
        parent = User.query.filter_by(login=form.parent_login.data).first()
        start_time = form.start_time.data
        duration = int(form.duration.data)
        finish_time = (start_time + datetime.timedelta(minutes=duration)).time()
        consultation.parent_id = getattr(parent, "id", None)
        consultation.date = form.date.data
        consultation.start_time = start_time.time()
        consultation.finish_time = finish_time
        consultation.is_free = form.is_free.data
        consultation.url = form.url.data
        db.session.commit()
        return redirect(url_for("main.teacher_consultations"))
    form.parent_login.data = consultation.parent.login if consultation.parent else ""
    form.date.data = consultation.date
    form.start_time.data = datetime.datetime(1900, 1, 1, consultation.start_time.hour,
                                             consultation.start_time.minute)
    form.duration.date = str((datetime.datetime(1900, 1, 1, consultation.finish_time.hour,
                                                consultation.finish_time.minute) - datetime.datetime(
        1900, 1, 1, consultation.start_time.hour,
        consultation.start_time.minute)).min)
    form.is_free.data = consultation.is_free
    form.url.data = consultation.url
    return render_template("teacher/manage_consultation.html", form=form,
                           header="Создать консультацию")


@auth.route("/teacher/consultations/delete/<int:consultation_id>", methods=["GET", "POST"])
@permissions_required(Permissions.MANAGE_CONSULTATIONS)
def delete_consultation(consultation_id):
    form = Agree()
    if form.validate_on_submit():
        if form.data["agree"]:
            try:
                consultation = db.session.query(Consultation).filter(Consultation.id == int(consultation_id)).first()
                db.session.delete(consultation)
                db.session.commit()
                flag = 1
            except Exception as ex:
                print(ex)
                flag = 0
            if flag == 1:
                flash("Консультация успешно удалена", category="success")
            elif flag == 0:
                flash("ПРОИЗОШЕЛ СБОЙ, пожалуйста, повторите попытку позже", category="error")
            return redirect(url_for("main.teacher_consultations"))
    return render_template("auth/auth.html", form=form,
                           header="Удаление консультации")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in set(['xlsx'])


@auth.route("/signup/parent/by_excel", methods=["GET", "POST"])
@permissions_required(Permissions.MANAGE_PARENTS)
def creating_parent_by_excel():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            if not os.access(UPLOAD_FOLDER, os.F_OK):
                os.mkdir(UPLOAD_FOLDER)
            filename = secure_filename(file.filename)
            timing = datetime.datetime.now().strftime("%H%M%S%f.%d%m%y")
            os.mkdir(os.path.join(UPLOAD_FOLDER, timing))
            file.save(os.path.join(UPLOAD_FOLDER, timing, filename))
            return redirect(url_for('auth.result_file_rendering',
                                    filename=filename, timing=timing))
    return render_template("auth/get_file.html")


@auth.route("/signup/parent/by_excel/result/<filename>/<timing>", methods=["GET", "POST"])
@permissions_required(Permissions.MANAGE_PARENTS)
def result_file_rendering(filename, timing):
    ex = data_parent_registration(os.path.join(UPLOAD_FOLDER, timing, filename), timing)
    os.remove(os.path.join(UPLOAD_FOLDER, timing, filename))
    os.rmdir(os.path.join(UPLOAD_FOLDER, timing))
    if ex.message == ExcelErrors.ERRORS_DICT[10]:
        return render_template("auth/suc_parent_reg.html",
                               header=ex.message, timing=timing)
    else:
        flash(ex.message, category="error")
        return redirect(url_for('auth.creating_parent_by_excel'))


@auth.route("/signup/parent/by_excel/download/<timing>", methods=["GET", "POST"])
@permissions_required(Permissions.MANAGE_PARENTS)
def download(timing):
    way = "excel\\reports\\" + timing
    return send_from_directory(way, timing + ".xlsx", environ=request.environ)
