from App.models import Staff
from App.database import db
from App.models import Student
from App.models import Request
from tabulate import tabulate


def create_staff_account(username, password):
    newuser = Staff(username=username, password=password)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def confirm_student_hours(student, hours):
    student.hours += hours
    db.session.commit()
    return student.hours

def view_pending_requests():
    pending_requests = db.session.query(Request, Student).join(Student).filter(Request.status == 'pending').all()
    table = [[req.Request.id, req.Student.username, req.Request.description, req.Request.number_of_hours] for req in pending_requests]
    headers = ["Request ID", "Student Username", "Description", "Number of Hours"]
    print(tabulate(table, headers, tablefmt="grid"))

def confirm_request(request_id, status):
    req = Request.query.get(request_id)
    if req:
        req.status = status
        student_id = req.student_id
        student = Student.query.get(student_id)
        confirm_student_hours(student, req.number_of_hours)
        db.session.commit()
        return True
    return False