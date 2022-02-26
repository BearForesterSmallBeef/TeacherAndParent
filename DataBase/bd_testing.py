from DataBase.DB import User, db


user1 = User()
user2 = User()

db.session.add(user1)
db.session.add(user2)
db.session.commit()

print(User.query.all())