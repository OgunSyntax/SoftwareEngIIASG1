from App.models import Staff
from App.database import db
from App.models import Student


def create_staff_account(username, password):
    newuser = Staff(username=username, password=password)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def confirm_student_hours(student, hours):
    student.hours += hours
    db.session.commit()
    return student.hours