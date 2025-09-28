# Flask Commands
# inside wsgi.py

Initilization
```python
#database populated with students,staff and hours
@app.cli.command("init", help="Creates and initializes the database")
def init():
   with app.app_context():
    initialize()
    print('database intialized')
```


User Command

<!-- veiw Leaderboard -->
```python

# view leaderboard regualr user without login 

@user_cli.command("view_leaderboard", help="unregistered users could view the leaderboard")
def leaderboard_view():
    leaderboard()
    return         
```
<!------>

Student/Saff commands


```Python
# Test users

# Student: Bob password: bobpass
# Staff: admin password: adminpass

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

            choice = input("Input 1 view Account\nInput 2 to view Leaderboard\nInput 3 to view Account/Accolades:\nInput 4 to make a request\nType 'exit' to log out\n: ")
            #Displays current student details
            if choice == '1':
                view_account(user.id)

            #Views all students with in a leaderboard format with the most hightest to lowest
            elif choice == '2':
                leaderboard()

            #view current Student Accolades
            elif choice == '3':
                view_accolades(user.id)
            
            #Make a request to log in a certain ammount of hours for community service/volunteering 
            elif choice == '4':
                description = input("Enter a description for your request: ")
                try:
                    number_of_hours = int(input("Enter the number of hours you are requesting to log: "))
                except ValueError:
                        print("Invalid input. Please enter a numeric value for hours.")
                make_request(user.id, description, number_of_hours)
                print("Request submitted successfully.")
               
            elif choice == 'exit':
                break
            else:
                print("Invalid choice. Please try again.")

        
    #staff capabilities 
    elif user and user.check_password(password) and user.type == 'staff':
        print(f'Welcome {username}!')


        while True:

            choice = input("Input 1 to Confirm Student Hours\nInput 2 to view Leaderboard\nInput 3 to view Pending Requests\nInput 4 to Confirm Requests\nType 'exit' to log out\n: ")

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

            #view 'pending' student requests
            elif choice == '3':
                view_pending_requests()

            #Confirm the requests made
            elif choice == '4':    
                while True:
                    confirm_request_id = input("Enter the Request ID to confirm: ")
                    status = input("Enter Y or N to change status (approved/denied): ").lower()
                    if status == 'y' or status == 'Y':
                        if confirm_request(confirm_request_id, "approved"):
                            print(f"Request {confirm_request_id} has been Approved.")
                            break
                        else:
                            print("Request not found.")

                    
                    elif status == 'n' or status == 'N':
                        print("Request Denied")
                        break
                    else:
                        print("Please type Y or N.")



            elif choice == 'exit':
                break
            else:
                print("Invalid choice. Please try again.\n")
    else:
        print('Invalid username or password\n')
```