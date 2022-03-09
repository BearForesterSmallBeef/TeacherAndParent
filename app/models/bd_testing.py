from app.models.DB import *  # https://stackoverflow.com/a/57789224
from app import create_app
from app import db
import os

app = create_app(os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig'))

with app.app_context():
    school1 = School()
    school1.name = '1501'
    school1.about = 'the best'
    school2 = School()
    school2.name = '486'
    school2.about = 'the worst'
#    for i in
#
#    db.session.add(user1)
#    db.session.add(user2)

    db.session.commit()
