from flask import Blueprint, render_template, request, redirect

from app import db
from app.models import Class, User, Parent, Consultation, TeacherSubjectsClasses, Subject, RolesIds
from app.auth.forms import *

main = Blueprint("main", __name__)


class ConsultationCard:
    fields_labels = (
        ("date", "Дата"),
        ("time", "Время"),
        ("duration", "Продолжительность"),
    )

    def __init__(self, consultation: Consultation):
        self.is_free = consultation.status
        self.date = consultation.date.strftime("%d.%m.%Y")
        self.time = consultation.start_time.strftime("%H:%M")
        self.duration = str(consultation.duration // 60) + " мин"


class ConsultationCardTeacher(ConsultationCard):
    fields_labels = ((("parent_name", "Родитель"), ) +
                     ConsultationCard.fields_labels +
                     (("class_", "Класс"), ))

    def __init__(self, consultation: Consultation):
        super(ConsultationCardTeacher, self).__init__(consultation)
        self.parent_name = consultation.parent.full_name if consultation.parent is not None else ""
        self.class_ = db.session.query(Parent).filter_by(
            user_id=consultation.parent_id
        ).first().class_.name if consultation.parent is not None else ""


class ConsultationCardParent(ConsultationCard):
    fields_labels = ((("teacher_name", "Учитель"), ) +
                     ConsultationCard.fields_labels)

    def __init__(self, consultation: Consultation):
        super(ConsultationCardParent, self).__init__(consultation)
        self.teacher_name = (consultation.teacher.full_name
                             if consultation.teacher is not None else "")


@main.route("/teachers")
def teacher_consultations():
    consultations = db.session.query(Consultation).all()
    consultation_cards = map(ConsultationCardTeacher, consultations)
    return render_template("teacher/consultations.html",
                           consultations=consultation_cards,
                           fields_labels=ConsultationCardTeacher.fields_labels)


@main.route("/parent/consultations")
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


@main.route("/parent_registration", methods=['GET', 'POST'])
def parent_registration():
    form = RegistrationParentForm()
    form.classes.choices = sorted([(i.name, i.name) for i in db.session.query(Class)],
                                  key=lambda x: int(x[0].split("-")[0]))
    if form.validate_on_submit():
        flag = create_parent(request.form["login"], request.form["password"], request.form["username"],
                             request.form["usersurename"], request.form["classes"],
                             middle_name=str(request.form["usermiddlename"]))
        return redirect(f"/reg_result/{flag}")
    return render_template("auth/parent_reg.html", form=form)


@main.route("/reg_result/<ok>", methods=['GET', 'POST'])
def reg_result(ok):
    form = BackToParentReg()
    flag = bool(int(ok))
    if form.validate_on_submit():
        return redirect("/parent_registration")
    return render_template("auth/reg_result.html", form=form, flag=flag)

