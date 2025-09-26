import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User, Student,Accolade
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize,create_student_account,confirm_student_hours,leaderboard,log_accolade_to_student,view_accolades,view_account)



# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
   with app.app_context():
    initialize()
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

@user_cli.command("create_student_account", help="Creates a student account")
@click.argument("username", default="student")
@click.argument("password", default="studentpass")
def create_student_account_command(username, password):
    create_student_account(username, password)
    print(f'Student account {username} created!')
# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

#view leaderboard regualr user without login
@user_cli.command("view_leaderboard", help="unregistered users could view the leaderboard")
def leaderboard_view():
    leaderboard()
    return         
#Login command
@user_cli.command("login", help="Login a user")
@click.argument("username", default="string")
@click.argument("password", default="string")

def login_user_command(username, password):
    username = input("Enter username: ")
    password = input("Enter password: ")
    user = User.query.filter_by(username=username).first()

    
    if user and user.check_password(password) and user.type == 'student':
        print(f'Welcome {username}!')

        while True:

            choice = input("Input 1 view Account\nInput 2 to view Leaderboard\nInput 3 to view Account/Accolades:\nType 'exit' to log out\n: ")

            if choice == '1':
                view_account(username)
            elif choice == '2':
                leaderboard()
            elif choice == '3':
                view_accolades(username)
            elif choice == 'exit':
                break
            else:
                print("Invalid choice. Please try again.")

        
    #staff capabilities 
    elif user and user.check_password(password) and user.type == 'staff':
        print(f'Welcome {username}!')


        while True:

            choice = input("Input 1 to Confirm Student Hours\nInput 2 to view Leaderboard\nType 'exit' to log out\n: ")

            #Confirming student hours
            if choice == '1':
                student_name = input("Enter the student's username: ")
                student = Student.query.filter_by(username=student_name).first()
                if student:
                    try:
                        hours = int(input("Enter number of hours to confirm: "))
                        new_total = confirm_student_hours(student, hours)
                        print(f"Confirmed {hours} hours for {student.username}. New total: {new_total} hours.")

                        # Check and award accolades if thresholds are met
                        for accolade in Accolade.query.all():
                            if new_total >= accolade.threshold:
                                existing_accolade = log_accolade_to_student(student.id, accolade.id)
                                if existing_accolade:
                                    print(f"Awarded accolade: {accolade.name}")

                    except ValueError:
                        print("Invalid input. Please enter a numeric value for hours.")
                else:
                    print("Student not found.")

            #viewing leaderboard
            elif choice == '2':
                 leaderboard()
            

            elif choice == 'exit':
                break
            else:
                print("Invalid choice. Please try again.\n")
    else:
        print('Invalid username or password\n')

    


app.cli.add_command(user_cli) # add the group to the cli

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)