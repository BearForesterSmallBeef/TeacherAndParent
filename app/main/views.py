from flask import Blueprint, render_template, request

from app import db
from app.models import Subject, User, RolesIds, TeacherSubjectsClasses

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
            "url": "https://zeem.com/2",
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


@main.route("/teacher/consultations")
def teacher_consultations():
    consultations = get_sample_teacher_consultations()
    return render_template("teacher/consultations.html", consultations=consultations)


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
