from flask import Blueprint, render_template, request

from app import db
from app.models import Subject, User, RolesIds, TeacherSubjectsClasses, Consultation, Parent

main = Blueprint("main", __name__)


def get_sample_teacher_consultations():
    import datetime
    from types import SimpleNamespace
    consultations = [
        {
            "is_free": False,
            "name": "Ирина Григорьевна",
            "date": datetime.date.today(),
            "time": (datetime.datetime.now()).time(),
            "form": 8,
            "url": "https://zeem.com/1",
        },
        {
            "is_free": True,
            "name": None,
            "date": datetime.date.today(),
            "time": (datetime.datetime.now() + datetime.timedelta(minutes=30)).time(),
            "form": None,
            "url": None,
        },
        {
            "is_free": False,
            "name": "Виталий Прошутто",
            "date": datetime.date.today() + datetime.timedelta(days=1),
            "time": (datetime.datetime.now() + datetime.timedelta(days=1)).time(),
            "form": 9,
            "url": "https://zeem.com/2",
        },
        {
            "is_free": False,
            "name": "Анастасия Землеройка",
            "date": datetime.date.today() + datetime.timedelta(days=1),
            "time": (datetime.datetime.now() + datetime.timedelta(days=1, minutes=30)).time(),
            "form": 9,
            "url": "https://zeem.com/3",
        }
    ]
    return [SimpleNamespace(**data) for data in consultations]


class ConsultationCard:
    fields_labels = {
        "parent_name": "Имя",
        "date": "Дата",
        "time": "Время",
        "duration": "Продолжительность",
        "class_": "Класс",
    }

    def __init__(self, consultation: Consultation):
        self.is_free = consultation.status
        self.parent_name = consultation.parent.full_name if consultation.parent is not None else ""
        self.date = consultation.consultation_start_time.date().strftime("%d.%m.%Y")
        self.time = consultation.consultation_start_time.time().strftime("%H:%M")
        self.duration = str((consultation.consultation_finish_time
                         - consultation.consultation_start_time).seconds // 60) + " мин"
        self.class_ = db.session.query(Parent).filter_by(
            parent_id=consultation.parent_id
        ).first().Class.name if consultation.parent is not None else ""
        # TODO: separate dates in consultation, add url to consultation
        # TODO: rename parent_id to user_id in Parent model


@main.route("/teacher/consultations")
def teacher_consultations():
    consultations = db.session.query(Consultation).all()
    consultation_cards = map(ConsultationCard, consultations)
    return render_template("teacher/consultations.html",
                           consultations=consultation_cards,
                           fields_labels=ConsultationCard.fields_labels)


@main.route("/parent/consultations")
def parent_consultations():
    teacher_id = request.args.get("teacher", type=int)
    consultations = db.session.query(Consultation)
    if teacher_id is not None:
        consultations = consultations.filter_by(teacher_id=teacher_id)
    consultation_cards = map(ConsultationCard, consultations)
    return render_template("teacher/consultations.html",
                           consultations=consultation_cards,
                           fields_labels=ConsultationCard.fields_labels)


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
