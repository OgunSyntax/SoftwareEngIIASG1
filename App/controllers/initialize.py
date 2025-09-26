from .user import create_user
from App.database import db
from .student import create_student_account
from .staff import create_staff_account
from .accolade import create_accolade, log_accolade_to_student
import csv
import random
from App.models import Accolade, Student




def initialize():
    db.drop_all()
    db.create_all()
    # initializing users from CSV
    with open('instance/users.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # skip header
        for row in reader:
            username, password, user_type = row
            if user_type == 'student':
                create_student_account(username.lower(), password)
            elif user_type == 'staff':
                create_staff_account(username.lower(), password)
    # create_student_account('bob', 'bobpass')
    # create_student_account('gibby', 'gibbypass')
    # create_staff_account('admin', 'adminpass')
   

   # initializing accolades  
    with open('instance/accolades.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # skip header
        for row in reader:
            name, description, threshold = row
            create_accolade(name, description, int(threshold))

    # Assign random hours to students for testing purposes
    for student in Student.query.all():
        random_hours = random.randint(0, 5000)
        student.hours = random_hours
        db.session.commit()
        for accolade in Accolade.query.all():
            if student.hours >= accolade.threshold:
                log_accolade_to_student(student.id, accolade.id)

        

    


    


