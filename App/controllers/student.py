from App.database import db
from App.models.student import Student
from tabulate import tabulate
from App.models.accolade import Accolade
from App.models.studentAccolade import StudentAccolade
from App.models.user import User

#creates student account
def create_student_account(username, password):
    newuser = Student(username=username, password=password)
    db.session.add(newuser)
    db.session.commit()
    return newuser


# display all students in a leaderboard format
def leaderboard():
     students = Student.query.order_by(Student.hours.desc()).all()
     table =[[i+1,s.username, s.hours] for i, s in enumerate(students)]
     headers = ["Position","Username", "Hours"]

     print(tabulate(table, headers, tablefmt="grid"))


#View students accolades
def view_accolades(username):
    students = Student.query.filter_by(username=username).all()
    if not students:
        print("No student found with that name.")
        return
    accolades = StudentAccolade.query.filter_by(student_id=students[0].id).all()
    if not accolades:
        print(f"{username} has no accolades.")
        return
    table = [[a.accolade.name, a.date_awarded.strftime("%Y-%m-%d")] for a in accolades]
    headers = ["Accolade", "Date Awarded"]

    print(tabulate(table, headers, tablefmt="grid"))
    
#View student account details
def view_account(username):
    student = Student.query.filter_by(username=username).first()
    if not student:
        print("No student found with that name.")
        return
    table = [[student.id,student.username, student.hours]]
    headers = ["ID","Username", "Total Hours"]
    print(tabulate(table, headers, tablefmt="grid"))



