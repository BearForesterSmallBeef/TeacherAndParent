from DB import *
from app import create_app
from app import db
import os

app = create_app(os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig'))

with app.app_context():
    school1 = School()
    school1.name = '1501'
    school1.about = 'На РЖД купил билет' \
                    'И жду свой рейс с кривым еблетом' \
                    'Нахуй нужен ваш автобус' \
                    'Ведь за мной прикатит Томас'
#    for i in
#
#    db.session.add(user1)
#    db.session.add(user2)

db.session.commit()
