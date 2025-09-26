from App.database import db
from App.models.accolade import Accolade
from App.models.student import Student

class StudentAccolade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    accolade_id = db.Column(db.Integer, db.ForeignKey('accolade.id'), nullable=False)
    date_awarded = db.Column(db.DateTime, nullable=False)

    student = db.relationship('Student', backref=db.backref('student_accolades', lazy=True))
    accolade = db.relationship('Accolade', backref=db.backref('student_accolades', lazy=True))

    def __init__(self, student_id, accolade_id, date_awarded):
        self.student_id = student_id
        self.accolade_id = accolade_id
        self.date_awarded = date_awarded

    def __repr__(self):
        return f'<StudentAccolade Student ID: {self.student_id}, Accolade ID: {self.accolade_id}>'