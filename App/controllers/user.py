from App.models import User,Student
from App.database import db
from tabulate import tabulate

def create_user(username, password):
    newuser = User(username=username, password=password)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def get_user_by_username(username):
    result = db.session.execute(db.select(User).filter_by(username=username))
    return result.scalar_one_or_none()

def get_user(id):
    return db.session.get(User, id)

def get_all_users():
    return db.session.scalars(db.select(User)).all()

def get_all_users_json():
    users = get_all_users()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        # user is already in the session; no need to re-add
        db.session.commit()
        return True
    return None

# display all students in a leaderboard format
def leaderboard():
     students = Student.query.order_by(Student.hours.desc()).all()
     table =[[i+1,s.username, s.hours] for i, s in enumerate(students)]
     headers = ["Position","Username", "Hours"]

     print(tabulate(table, headers, tablefmt="grid"))
