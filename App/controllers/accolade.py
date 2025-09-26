from App.models.accolade import Accolade
from App.database import db
from App.models.student import Student
from App.models.studentAccolade import StudentAccolade

def create_accolade(name, description, threshold):
        new_accolade = Accolade(name=name, description=description, threshold=threshold)
        db.session.add(new_accolade)
        db.session.commit()
        return new_accolade

def log_accolade_to_student(student_id, accolade_id):
    student = Student.query.get(student_id)
    accolade = Accolade.query.get(accolade_id)
    if student and accolade:
        student_accolade = StudentAccolade(student_id=student_id, accolade_id=accolade_id, date_awarded=db.func.now())
        db.session.commit()
        db.session.add(student_accolade)
        return student_accolade
    