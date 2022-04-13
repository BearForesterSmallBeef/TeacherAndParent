from flask import Blueprint, render_template, request, redirect, url_for, Markup, g
from flask_login import current_user, login_required

from app import db
from app.models import User, Parent, Consultation, TeacherSubjectsClasses, Subject, RolesIds
from app.auth.utils import roles_required

main = Blueprint("main", __name__)


@main.before_request
def change_navbar():
    if not current_user.is_authenticated:
        return
    if current_user.role_id == RolesIds.TEACHER:
        g.nav_items = [("auth.signup", "Регистрация")]
    elif current_user.role_id == RolesIds.PARENT:
        g.nav_items = [("main.get_subjects", "Предметы"), ("main.get_teachers", "Учителя")]


class ConsultationCard:
    fields_labels = (
        ("date", "Дата"),
        ("time", "Время"),
        ("duration", "Продолжительность"),
        ("url", "Ссылка"),
    )

    def __init__(self, consultation: Consultation):
        self.is_free = consultation.status
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
        self.class_ = db.session.query(Parent).filter_by(
            user_id=consultation.parent_id
        ).first().class_.name if consultation.parent is not None else ""


class ConsultationCardParent(ConsultationCard):
    fields_labels = ((("teacher_name", "Учитель"),) +
                     ConsultationCard.fields_labels)

    def __init__(self, consultation: Consultation):
        super(ConsultationCardParent, self).__init__(consultation)
        self.teacher_name = (consultation.teacher.full_name
                             if consultation.teacher is not None else "")


@main.route("/teacher/consultations")
@roles_required("teacher")
def teacher_consultations():
    consultations = db.session.query(Consultation).all()
    consultation_cards = map(ConsultationCardTeacher, consultations)
    return render_template("teacher/consultations.html",
                           consultations=consultation_cards,
                           fields_labels=ConsultationCardTeacher.fields_labels)


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
                           fields_labels=ConsultationCardParent.fields_labels)


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
        return redirect(url_for(".index"))


@main.route("/about")
def about():
    return render_template("about.html")


@main.route("/")
def index():
    return render_template("index.html")
