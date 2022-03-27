import os

from werkzeug.security import generate_password_hash

from app import create_app
from app.models import *

app = create_app(os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig'))

with app.app_context():
    object_list = ["русский язык",
                   "программирование на c++",
                   "практикум",
                   "черчение",
                   "обществознание",
                   "ОДНРК",
                   "ОБЖ",
                   "литература",
                   "сквозной курс",
                   "география",
                   "геометрия",
                   "физика",
                   "физкультура",
                   "компютерная графика",
                   "биология",
                   "астраномия",
                   "алгебра",
                   "английский язык",
                   "история",
                   "информатика",
                   "химия"]
    for i in object_list:
        db.session.add(Subject(name=i, about=f"Школьный предмет: {i}"))

    class_list = ["9-2",
                  "11-4",
                  "9-1",
                  "9-4",
                  "8-3",
                  "10-5",
                  "10-3",
                  "9-5",
                  "10-4",
                  "11-3",
                  "11-1",
                  "7-1",
                  "10-1",
                  "8-1",
                  "7-3",
                  "11-5",
                  "8-2",
                  "7-2",
                  "8-4",
                  "10-2",
                  "11-2",
                  "9-3",
                  "9-6"]
    for i in class_list:
        db.session.add(Class(name=i, about=f"Класс {i} конечно хорош, но 9-4 лучше"))

    db.session.add(Role(name="admin", about="Может все - царь-батюшка"))
    db.session.add(
        Role(name="head_teacher", about="Может создавать учетные записи - почти царь всея Руси"))
    db.session.add(Role(name="developers", about="Цари всея Руси"))
    db.session.add(Role(name="teacher", about="Может создавать консультации"))
    db.session.add(Role(name="parent", about="Может записываться на консультации"))

    db.session.add(
        User(login="timonich_login", hashed_password=generate_password_hash("timonich_password"),
             name="Татьяна",
             surname="Тимонич", middle_name="Васильевна",
             role_id=db.session.query(Role).filter(Role.name == "head_teacher").first().id))

    db.session.add(
        User(login="teacher1_login", hashed_password=generate_password_hash("teacher1_password"),
             name="Иван",
             surname="Иванов", middle_name="Иванович",
             role_id=db.session.query(Role).filter(Role.name == "teacher").first().id))
    db.session.add(
        User(login="teacher2_login", hashed_password=generate_password_hash("teacher2_password"),
             name="Пётр",
             surname="Петров", middle_name="Пётрович",
             role_id=db.session.query(Role).filter(Role.name == "teacher").first().id))

    db.session.add(
        User(login="parent1_login", hashed_password=generate_password_hash("parent1_password"),
             name="Василий",
             surname="Васильев", middle_name="Васильевич",
             role_id=db.session.query(Role).filter(Role.name == "parent").first().id))
    db.session.add(
        User(login="parent2_login", hashed_password=generate_password_hash("parent2_password"),
             name="Семён",
             surname="Смирнов", middle_name="Семёнович",
             role_id=db.session.query(Role).filter(Role.name == "parent").first().id))

    db.session.add(
        Parent(parent_id=db.session.query(User).filter(User.surname == "Васильев").first().id,
               class_id=db.session.query(Class).filter(Class.name == "9-4").first().id))
    db.session.add(
        Parent(parent_id=db.session.query(User).filter(User.surname == "Смирнов").first().id,
               class_id=db.session.query(Class).filter(Class.name == "9-5").first().id))

    for i in range(len(class_list) // 2):
        db.session.add(TeacherSubjectsClasses(
            teacher_id=db.session.query(User).filter(User.surname == "Петров").first().id,
            subject_id=db.session.query(Subject).filter(Subject.name == object_list[0]).first().id,
            class_id=db.session.query(Class).filter(Class.name == class_list[i]).first().id))
        db.session.add(TeacherSubjectsClasses(
            teacher_id=db.session.query(User).filter(User.surname == "Иванов").first().id,
            subject_id=db.session.query(Subject).filter(Subject.name == object_list[1]).first().id,
            class_id=db.session.query(Class).filter(Class.name == class_list[i]).first().id))
    for i in range(len(class_list) // 2, len(class_list)):
        db.session.add(TeacherSubjectsClasses(
            teacher_id=db.session.query(User).filter(User.surname == "Петров").first().id,
            subject_id=db.session.query(Subject).filter(Subject.name == object_list[1]).first().id,
            class_id=db.session.query(Class).filter(Class.name == class_list[i]).first().id))
        db.session.add(TeacherSubjectsClasses(
            teacher_id=db.session.query(User).filter(User.surname == "Иванов").first().id,
            subject_id=db.session.query(Subject).filter(Subject.name == object_list[0]).first().id,
            class_id=db.session.query(Class).filter(Class.name == class_list[i]).first().id))

    db.session.add(Consultation(
        teacher_id=db.session.query(User).filter(User.surname == "Петров").first().id,
        parent_id=db.session.query(User).filter(User.surname == "Васильев").first().id,
        consultation_start_time=datetime.datetime(2023, 1, 10, 13, 30, 0),
        consultation_finish_time=datetime.datetime(2023, 1, 10, 13, 30, 0) + datetime.timedelta(
            minutes=10),
        status=False))
    db.session.add(Consultation(
        teacher_id=db.session.query(User).filter(User.surname == "Петров").first().id,
        consultation_start_time=datetime.datetime(2023, 1, 10, 13, 40, 0),
        consultation_finish_time=datetime.datetime(2023, 1, 10, 13, 40, 0) + datetime.timedelta(
            minutes=10)))

    db.session.add(Consultation(
        teacher_id=db.session.query(User).filter(User.surname == "Иванов").first().id,
        parent_id=db.session.query(User).filter(User.surname == "Смирнов").first().id,
        consultation_start_time=datetime.datetime(2023, 1, 10, 13, 30, 0),
        consultation_finish_time=datetime.datetime(2023, 1, 10, 13, 30, 0) + datetime.timedelta(
            minutes=10),
        status=False))
    db.session.add(Consultation(
        teacher_id=db.session.query(User).filter(User.surname == "Иванов").first().id,
        consultation_start_time=datetime.datetime(2023, 1, 10, 13, 40, 0),
        consultation_finish_time=datetime.datetime(2023, 1, 10, 13, 40, 0) + datetime.timedelta(
            minutes=10)))
    db.session.commit()
