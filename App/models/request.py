from App.database import db


class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    description = db.Column(db.String(200), nullable=False)  # Description of the request
    number_of_hours = db.Column(db.Integer, nullable=False)  # Number of hours requested
    status = db.Column(db.String(20), nullable=False, default='pending')  # pending, approved, denied

    def __init__(self, student_id, description, status='pending', number_of_hours=0):
        self.student_id = student_id
        self.description = description
        self.status = status
        self.number_of_hours = number_of_hours

    def __repr__(self):
        return f'<Request {self.id} - Student {self.student_id} - Status {self.status}>'