from App.database import db
from App.models.student import Student
from tabulate import tabulate
from App.models.accolade import Accolade
from App.models.studentAccolade import StudentAccolade
from App.models.user import User
from App.models.request import Request

#creates student account
def create_student_account(username, password):
    newuser = Student(username=username, password=password)
    db.session.add(newuser)
    db.session.commit()
    return newuser





#View students accolades
def view_accolades(id):
    students = Student.query.filter_by(id=id).first()
    if not students:
        print("No student found with that name.")
        return
    accolades = StudentAccolade.query.filter_by(student_id= students.id).all()
    if not accolades:
        print(f"{students.username} has no accolades.")
        return
    table = [[a.accolade.name, a.date_awarded.strftime("%Y-%m-%d")] for a in accolades]
    headers = ["Accolade", "Date Awarded"]

    print(tabulate(table, headers, tablefmt="grid"))
    
#View student account details
def view_account(id):
    student = Student.query.filter_by(id=id).first()
    if not student:
        print("No student found with that name.")
        return
    table = [[student.id,student.username, student.hours]]
    headers = ["ID","Username", "Total Hours"]
    print(tabulate(table, headers, tablefmt="grid"))


def make_request(student_id, description, number_of_hours):
    new_request = Request(student_id=student_id, description=description, number_of_hours=number_of_hours)
    db.session.add(new_request)
    db.session.commit()
    return new_request





