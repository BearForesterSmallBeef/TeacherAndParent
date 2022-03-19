from app.models import *
from app import create_app
from app import db
import os

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
        db.session.add(Object(name=i, about=f"Школьный предмет: {i}"))

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

    db.session.add(Role(name="admin", about="Может создавать учетные записи - почти царь всея Руси"))
    db.session.add(Role(name="developers", about="Цари всея Руси"))
    db.session.add(Role(name="teacher", about="Может создавать консультации"))
    db.session.add(Role(name="parent", about="Может записываться на консультации"))
    db.session.add(Role(name="guest", about="Вы кто такие?"))
    db.session.commit()

