from App.database import db
from .user import User


class Student(User):
   

    __tablename__ = 'student'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    hours = db.Column(db.Integer, default=0)
    __mapper_args__ = {
        'polymorphic_identity': 'student',
    }

    def __init__(self, username, password):
        super().__init__(username=username, password=password)  
        self.hours = 0


    def __repr__(self):
        return f'<Student {self.username}>'
    
