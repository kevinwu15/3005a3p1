import psycopg2
from config import getFields
from datetime import date

# Function called in main to display all students by performing a SELECT sql query on the database
def getAllStudents():
    global conn
    # From psycopg2 documentation https://www.psycopg.org/docs/connection.html
    with conn:
        with conn.cursor() as curs:
            curs.execute('SELECT * FROM "students";')
            print(curs.fetchall())
            # close cursor when done
            curs.close()

# Function called in main to add a new student by performing an INSERT sql query on the database
def addStudent(first_name, last_name, email, enrollment_date):
    global conn
    with conn:
        with conn.cursor() as curs:
            curs.execute('INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES (%s, %s, %s, %s);', ((first_name, last_name, email, enrollment_date)))
            curs.close()

# Function called in main to update the email of a student by performing an UPDATE WHERE sql query on the database
def updateStudentEmail(student_id, new_email):
    global conn
    with conn:
        with conn.cursor() as curs:
            curs.execute('UPDATE students SET email = %s WHERE student_id = %s', ((new_email, student_id)))
            curs.close()

# Function called in main to delete a specified student by performing a DELETE WHERE sql query on the database
def deleteStudent(student_id):
    global conn
    with conn:
        with conn.cursor() as curs:
            curs.execute('DELETE FROM students WHERE student_id = %s', ((student_id,)))
            curs.close()

# Function called in main to repopulate the database with the default information, including resetting the primary key back to 1
def resetDatabaseToDefault():
    global conn
    with conn:
            with conn.cursor() as curs:
                # Remove all current rows
                curs.execute("TRUNCATE TABLE students")
                # Reset primary id back to 1
                curs.execute("ALTER SEQUENCE students_student_id_seq RESTART WITH 1")
                # Repopulate the table using the initial data query provided in the assignment spec
                curs.execute("INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES ('John', 'Doe', 'john.doe@example.com', '2023-09-01'), ('Jane', 'Smith', 'jane.smith@example.com', '2023-09-01'), ('Jim', 'Beam', 'jim.beam@example.com', '2023-09-02');")
                curs.close()

if __name__ == "__main__":
    # Attempting to connect to the database by using the psycopg2 connect
    try:
        fields = getFields()
        print("Connecting to COMP3005 A3 database")
        # Unpacking the fields dictionary into parameters for the connect function
        # trying to assign a new connection
        conn = psycopg2.connect(**fields)
        resetDatabaseToDefault()
        # Prompt user to call functions
        while True:
            num = input("Options (enter a number): \n1. View students\n2. Add student\n3. Update student email\n4. Delete student\n5. Exit session\n")
            match num:
                case "1":
                    getAllStudents()
                case "2":
                    try:
                        print("New student information")
                        first_name = input("First name: ")
                        last_name = input("Last name: ")
                        email = input("Email: ")
                        year = int(input("Enrollment year: "))
                        month = int(input("Enrollment month: "))
                        day = int(input("Enrolmment day: "))
                        addStudent(first_name, last_name, email, date(year, month, day))
                    except ValueError:
                        print("Invalid input")
                case "3":
                    try:
                        student_id = int(input("Student id of student to update: "))
                        email = input("Updated email: ")
                        updateStudentEmail(student_id, email)
                    except ValueError:
                        print("Invalid input")
                case "4":
                    try:
                        student_id = int(input("Student id of student to delete: "))
                        deleteStudent(student_id)
                    except ValueError:
                        print("Invalid input")
                case "5":
                    break
                case _:
                    print("Enter a valid option")
    # Catch error if database connection unsuccessful
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    # Close connection to database at the end
    finally:
        print("Closing connection to database")
        conn.close()