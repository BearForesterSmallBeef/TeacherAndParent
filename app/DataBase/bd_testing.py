from DB import User
from app import create_app
from app import db
import os

app = create_app(os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig'))

with app.app_context():
    user1 = User()
    user2 = User()

    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    print(User.query.all())
