from flask import Blueprint, render_template, request, redirect, url_for, Markup, g, flash
from flask_login import current_user, login_required

from app import db
from app.auth.utils import roles_required
from app.models import (User, Parent, Consultation, TeacherSubjectsClasses, Subject, RolesIds,
                        Permissions)

main = Blueprint("main", __name__)


@main.before_app_request
def change_navbar():
    if not current_user.is_authenticated:
        return
    g.nav_items = []
    if current_user.can(Permissions.MANAGE_OBJECTS):
        g.nav_items.extend([("auth.add", "Добавление"), ])
    if current_user.can(Permissions.MANAGE_PARENTS):  # кто ХОТЯ БЫ может создать пользоваетлей
        g.nav_items.extend([("auth.signup", "Регистрация"), ("auth.delete", "Удаление"),
                            ("auth.creating_parent_by_excel", "Загрузка файла")])
    if current_user.role_id == RolesIds.PARENT:
        g.nav_items.extend([("main.get_subjects", "Предметы"), ("main.get_teachers", "Учителя")])
    role_label_mapping = {"parent": "Родитель",
                          "teacher": "Учитель",
                          "head_teacher": "Завуч",
                          "admin": "Админ", }
    g.nav_user_role = role_label_mapping.get(current_user.role.name)
    g.nav_items.append(("flask-apispec.swagger-ui", "API"))


class ConsultationCard:
    fields_labels = (
        ("date", "Дата"),
        ("time", "Время"),
        ("duration", "Продолжительность"),
        ("url", "Ссылка"),
    )

    def __init__(self, consultation: Consultation):
        self.consultation_id = consultation.id
        self.parent_id = consultation.parent_id
        self.is_free = consultation.is_free
        self.date = consultation.date.strftime("%d.%m.%Y")
        self.time = consultation.start_time.strftime("%H:%M")
        self.duration = str(consultation.duration // 60) + " мин"
        url = consultation.url if consultation.url is not None else ""
        self.url = Markup(f"<a href='{url}'>{url}</a>")


class ConsultationCardTeacher(ConsultationCard):
    fields_labels = ((("parent_name", "Родитель"),) +
                     ConsultationCard.fields_labels +
                     (("class_", "Класс"),))

    def __init__(self, consultation: Consultation):
        super(ConsultationCardTeacher, self).__init__(consultation)
        self.parent_name = consultation.parent.full_name if consultation.parent is not None else ""
        parent = db.session.query(Parent).filter_by(
            user_id=consultation.parent_id
        ).first()
        class_ = getattr(parent, "class_", None)
        self.class_ = f"{class_.parallel}-{class_.groups}" if class_ is not None else ""


class ConsultationCardParent(ConsultationCard):
    fields_labels = ((("teacher_name", "Учитель"),) +
                     ConsultationCard.fields_labels)

    def __init__(self, consultation: Consultation):
        super(ConsultationCardParent, self).__init__(consultation)
        self.teacher_name = (consultation.teacher.full_name
                             if consultation.teacher is not None else "")
        if current_user.id != consultation.parent_id:
            self.url = ""


@main.route("/teacher/consultations")
@roles_required("teacher")
def teacher_consultations():
    consultations = db.session.query(Consultation).all()
    consultation_cards = map(ConsultationCardTeacher, consultations)
    return render_template("teacher/consultations.html",
                           consultations=consultation_cards,
                           fields_labels=ConsultationCardTeacher.fields_labels,
                           PARENT=RolesIds.PARENT)


@main.route("/parent/consultations")
@roles_required("parent")
def parent_consultations():
    teacher_id = request.args.get("teacher", type=int)
    consultations = db.session.query(Consultation)
    if teacher_id is not None:
        consultations = consultations.filter_by(teacher_id=teacher_id)
    consultation_cards = map(ConsultationCardParent, consultations)
    return render_template("parent/consultations.html",
                           consultations=consultation_cards,
                           fields_labels=ConsultationCardParent.fields_labels,
                           PARENT=RolesIds.PARENT)


@main.route("/subjects")
def get_subjects():
    subjects = db.session.query(Subject).all()
    return render_template("parent/subjects.html", subjects=subjects)


@main.route("/teachers")
def get_teachers():
    teachers = db.session.query(User).filter(User.role_id == RolesIds.TEACHER)
    subject_id = request.args.get("subject", type=int)
    if subject_id is not None:
        teachers = teachers.join(
            TeacherSubjectsClasses.query.join(
                Subject, TeacherSubjectsClasses.subject_id == subject_id
            )
        )
    return render_template("parent/teachers.html", teachers=teachers)


@main.route("/consultations")
@login_required
def get_consultations():
    if current_user.role_id == RolesIds.TEACHER:
        return redirect(url_for(".teacher_consultations"))
    elif current_user.role_id == RolesIds.PARENT:
        return redirect(url_for(".parent_consultations"))
    else:
        flash("Вы не имеете доступ к консультациям. Выберите пункт в меню.", category="error")
        return redirect(url_for(".index"))


@main.route("/schedule/<int:consultation_id>", methods=["POST"])
@roles_required("parent")
def schedule_consultation(consultation_id):
    consultation = Consultation.query.get(consultation_id)
    if consultation is None:  # если вручную перешли по адресу
        flash("Такой консультации не существует", category="error")
        return redirect(url_for(".get_consultations"), 303)
    elif not consultation.is_free:
        flash("Консультация уже знанята", category="error")
        return redirect(url_for(".get_consultations"), 303)
    consultation.parent_id = current_user.id
    consultation.is_free = False
    db.session.commit()
    flash("Вы успешно записались на консультацию", category="success")
    return redirect(url_for(".get_consultations"), 303)


@main.route("/cancel/<int:consultation_id>", methods=["POST"])
@roles_required("parent")
def cancel_consultation(consultation_id):
    consultation = Consultation.query.get(consultation_id)
    if consultation is None:  # если вручную перешли по адресу
        flash("Такой консультации не существует", category="error")
        return redirect(url_for(".get_consultations"), 303)
    elif consultation.is_free:
        flash("Нельзя отписаться от незанетой консультации", category="error")
        return redirect(url_for(".get_consultations"), 303)
    elif consultation.parent_id != current_user.id:
        flash("Вы не записывались на эту консультацию", category="error")
        return redirect(url_for(".get_consultations"), 303)
    consultation.parent_id = None
    consultation.is_free = True
    db.session.commit()
    flash("Вы успешно отпилась от консультацию", category="success")
    return redirect(url_for(".get_consultations"), 303)


@main.route("/about")
def about():
    return render_template("about.html")


@main.route("/")
def index():
    return render_template("index.html")
