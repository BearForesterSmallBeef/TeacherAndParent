import os

from app import create_app
from app import db

app = create_app(os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig'))

with app.app_context():
    print(db.metadata.tables.keys())
    for i in db.metadata.tables.keys():
        print(i)
        print("*" * 50)
        for j in db.session.query(db.metadata.tables[i]):
            print(j)
        print("_" * 50)
        print("\n" * 3)
