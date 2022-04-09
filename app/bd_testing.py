from app import create_app
from app.models import *

app = create_app('config.DevelopmentConfig')

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

    Role.insert_roles()

    db.session.add(
        User(login="timonich_login", password="timonich_password",
             name="Татьяна",
             surname="Тимонич", middle_name="Васильевна",
             role_id=db.session.query(Role).filter(Role.name == "head_teacher").first().id))

    db.session.add(
        User(login="teacher1_login", password="teacher1_password",
             name="Иван",
             surname="Иванов", middle_name="Иванович",
             role_id=db.session.query(Role).filter(Role.name == "teacher").first().id))
    db.session.add(
        User(login="teacher2_login", password="teacher2_password",
             name="Пётр",
             surname="Петров", middle_name="Пётрович",
             role_id=db.session.query(Role).filter(Role.name == "teacher").first().id))

    db.session.add(
        User(login="parent1_login", password="parent1_password",
             name="Василий",
             surname="Васильев", middle_name="Васильевич",
             role_id=db.session.query(Role).filter(Role.name == "parent").first().id))
    db.session.add(
        User(login="parent2_login", password="parent2_password",
             name="Семён",
             surname="Смирнов", middle_name="Семёнович",
             role_id=db.session.query(Role).filter(Role.name == "parent").first().id))

    db.session.add(
        Parent(user_id=db.session.query(User).filter(User.surname == "Васильев").first().id,
               class_id=db.session.query(Class).filter(Class.name == "9-4").first().id))
    db.session.add(
        Parent(user_id=db.session.query(User).filter(User.surname == "Смирнов").first().id,
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
        date=datetime.date(2023, 1, 10),
        start_time=datetime.time(13, 30, 0),
        finish_time=(datetime.datetime.combine(datetime.date.min,
                                               datetime.time(13, 30, 0)) + datetime.timedelta(
            minutes=10)).time(),
        status=False,
        url="https://zeem.com/1"
    ))
    db.session.add(Consultation(
        teacher_id=db.session.query(User).filter(User.surname == "Петров").first().id,
        date=datetime.date(2023, 1, 10),
        start_time=datetime.time(13, 40, 0),
        finish_time=(datetime.datetime.combine(datetime.date.min,
                                               datetime.time(13, 40, 0)) + datetime.timedelta(
            minutes=10)).time()))

    db.session.add(Consultation(
        teacher_id=db.session.query(User).filter(User.surname == "Иванов").first().id,
        parent_id=db.session.query(User).filter(User.surname == "Смирнов").first().id,
        date=datetime.date(2023, 1, 10),
        start_time=datetime.time(13, 30, 0),
        finish_time=(datetime.datetime.combine(datetime.date.min,
                                               datetime.time(13, 30, 0)) + datetime.timedelta(
            minutes=10)).time(),
        status=False,
        url="https://zeem.com/2"
    ))
    db.session.add(Consultation(
        teacher_id=db.session.query(User).filter(User.surname == "Иванов").first().id,
        date=datetime.date(2023, 1, 10),
        start_time=datetime.time(13, 40, 0),
        finish_time=(datetime.datetime.combine(datetime.date.min,
                                               datetime.time(13, 40, 0)) + datetime.timedelta(
            minutes=10)).time()))
    db.session.commit()
