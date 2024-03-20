from flask import Flask, render_template, request ,redirect, url_for, session,jsonify  # Import render_template
from flask_bcrypt import Bcrypt, check_password_hash #pip install Flask-Bcrypt = https://pypi.org/project/Flask-Bcrypt/
from flask_restful import Resource, Api
from flask_jwt_extended import create_access_token,JWTManager

import re

from model import db, User, Student,Teacher

app = Flask(__name__)

app.config['SECRET_KEY'] = 'cairocoders-ednalan'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flaskdb.db'
# Databse configuration mysql                             Username:password@hostname/databasename
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost/attendance-system'
  
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

bcrypt = Bcrypt(app) 
api = Api(app)
jwt = JWTManager(app)
   

db.init_app(app)
with app.app_context():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def start():
    return render_template('welcome_screen.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        print(email)
        print(password)
        if email == '' or password == '':
            message = 'Please enter email and password !'
        else:
            user = User.query.filter_by(email=email).first()
            print(user)
            if user is None:
                message = 'Please enter correct email / password !'
            else:
                
                 if not bcrypt.check_password_hash(user.password, password):
                    message = 'Please enter correct email and password !'
                 else:    
                    session['loggedin'] = True
                    session['userid'] = user.id
                    session['name'] = user.name
                    session['email'] = user.email
                    message = 'Logged in successfully !'           
                    return redirect(url_for('dashboard'))
    return render_template('login.html', message = message)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    message = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form :
        fullname = request.form['name']
        password = request.form['password']
        email = request.form['email']
        print(fullname)
        print(password)
        print(email)
        user_exists = User.query.filter_by(email=email).first() is not None
       
        if user_exists:
            message = 'Email already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            message = 'Invalid email address !'
        elif not fullname or not password or not email:
            message = 'Please fill out the form !'
        else:
            hashed_password = bcrypt.generate_password_hash(password)
            new_user = User(name=fullname, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()          
            message = 'You have successfully registered!'
    elif request.method == 'POST':
        message = 'Please fill out the form !'
    return render_template('signup.html', message = message)





@app.route('/add_students', methods=['GET', 'POST'])
def add_students():
    message = ''
    if request.method == 'POST' and 'name' in request.form and 'email' in request.form and 'password' in request.form and 'registrationNo' in request.form and 'gender' in request.form and 'department' in request.form and 'technology' in request.form and 'semester' in request.form and 'number' in request.form:
        fullname = request.form['name']
        password = request.form['password']
        email = request.form['email']
        registrationNo = request.form['registrationNo']
        gender =  request.form['gender']
        department = request.form['department'] 
        technology = request.form['technology']
        semester =  request.form['semester']
        number =  request.form['number']
        print(fullname)
        print(password)
        print(email)
        student_exists = Student.query.filter_by(email=email).first() is not None
       
        if student_exists:
            message = 'Email already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            message = 'Invalid email address !'
        elif not fullname or not password or not email:
            message = 'Please fill out the form !'
        else:
            hashed_password = bcrypt.generate_password_hash(password)
            new_student = Student(name=fullname, email=email, password=hashed_password,registrationNo=registrationNo,gender=gender,department=department,technology=technology,semester=semester,number=number)
            db.session.add(new_student)
            db.session.commit()          
            message = 'Student have successfully registered!'
    elif request.method == 'POST':
        message = 'Please fill out the form !'
    return render_template('add_students.html',message = message)

@app.route('/add_teachers', methods=['GET', 'POST'])
def add_teachers():
    message = ''
    if request.method == 'POST' and 'name' in request.form and 'email' in request.form and 'password' in request.form and 'registrationNo' in request.form and 'gender' in request.form and 'department' in request.form and 'number' in request.form:
        fullname = request.form['name']
        password = request.form['password']
        email = request.form['email']
        registrationNo = request.form['registrationNo']
        gender =  request.form['gender']
        department = request.form['department'] 
        number =  request.form['number']
        print(fullname)
        print(password)
        print(email)
        teacher_exists = Teacher.query.filter_by(email=email).first() is not None
       
        if teacher_exists:
            message = 'Email already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            message = 'Invalid email address !'
        elif not fullname or not password or not email:
            message = 'Please fill out the form !'
        else:
            hashed_password = bcrypt.generate_password_hash(password)
            new_teacher = Teacher(name=fullname, email=email, password=hashed_password,registrationNo=registrationNo,gender=gender,department=department,number=number)
            db.session.add(new_teacher)
            db.session.commit()          
            message = 'Teacher have successfully registered!'
    elif request.method == 'POST':
        message = 'Please fill out the form !'
    return render_template('add_teachers.html',message=message)




# class StudentRegistration(Resource):
#     def post(self):

#         message = ''
#         data = request.get_json()
#         name = data.get('name')
#         password = data.get('password')
#         email = data.get('email')
#         registrationNo = data.get('registrationNo')
#         gender = data.get('gender')
#         department = data.get('department')
#         technology = data.get('technology')
#         semester = data.get('semester')
#         number = data.get('number')

#         # Check if email already exists
#         student_exists = Student.query.filter_by(email=email).first()
#         if student_exists:
#             message = 'Email already exists!'
#             return jsonify(message=message), 400  # Return error response
#         elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
#             message = 'Invalid email address!'
#             return jsonify(message=message), 400  # Return error response
#         elif not all([name, password, email, registrationNo, gender, department, technology, semester, number]):
#             message = 'Please fill out all fields!'
#             return jsonify(message=message), 400  # Return error response
#         else:
#             # Create a new Student object
#             new_student = Student(name=name, email=email, password=password, registrationNo=registrationNo,
#                                   gender=gender, department=department, technology=technology, semester=semester,
#                                   number=number)

#             # Add the new student to the database session
#             db.session.add(new_student)

#             # Commit the session to persist changes
#             db.session.commit()

#             message = 'Student has been successfully registered!'
#             return jsonify(message=message), 200  # Return success response

#     def get(self):
#         # Your GET method implementation
#         # This can be used for rendering an HTML form or providing additional information
#         return jsonify(message="GET method for student registration endpoint")


# class TeacherRegistration(Resource):
#     def post(self):

#         message = ''
#         data = request.get_json()
#         name = data.get('name')
#         password = data.get('password')
#         email = data.get('email')
#         registrationNo = data.get('registrationNo')
#         gender = data.get('gender')
#         department = data.get('department')
#         number = data.get('number')

#         # Check if email already exists
#         student_exists = Teacher.query.filter_by(email=email).first()
#         if student_exists:
#             message = 'Email already exists!'
#             return jsonify(message=message), 400  # Return error response
#         elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
#             message = 'Invalid email address!'
#             return jsonify(message=message), 400  # Return error response
#         elif not all([name, password, email, registrationNo, gender, department, number]):
#             message = 'Please fill out all fields!'
#             return jsonify(message=message), 400  # Return error response
#         else:
#             # Create a new Student object
#             new_teacher = Teacher(name=name, email=email, password=password, registrationNo=registrationNo,
#                                   gender=gender, department=department,
#                                   number=number)

#             # Add the new student to the database session
#             db.session.add(new_teacher)

#             # Commit the session to persist changes
#             db.session.commit()

#             message = 'Teacher has been successfully registered!'
#             return jsonify(message=message), 200  # Return success response

#     def get(self):
#         # Your GET method implementation
#         # This can be used for rendering an HTML form or providing additional information
#         return jsonify(message="GET method for teacher registration endpoint")



class TeacherRegistration(Resource):
    def post(self):
        message = ''
        data = request.get_json()

        name = data.get('name')
        password = data.get('password')
        email = data.get('email')
        registrationNo = data.get('registrationNo')
        gender = data.get('gender')
        department = data.get('department')
        number = data.get('number')

        # Check if email already exists
        teacher_exists = Teacher.query.filter_by(email=email).first()
        if teacher_exists:
            message = 'Email already exists!'
            return jsonify({'message': message}), 400

        # Validate email format
        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            message = 'Invalid email address!'
            return jsonify({'message': message}), 400

        # Check if all fields are provided
        if not all([name, password, email, registrationNo, gender, department, number]):
            message = 'Please fill out all fields!'
            return jsonify({'message': message}), 400

        # Create a new Teacher object
        new_teacher = Teacher(name=name, email=email, password=password, registrationNo=registrationNo,
                              gender=gender, department=department, number=number)

        # Add the new teacher to the database session
        db.session.add(new_teacher)

        # Commit the session to persist changes
        db.session.commit()

        message = 'Teacher has been successfully registered!'
        return jsonify({'message': message}), 200



# class StudentLogin(Resource):
#     def post(self):  
#         data = request.get_json()
#         email = data['email']
#         password =data['password']
        
#         student = Student.query.filter_by(email=email).first()
#         #Check if both email and password are provided
#         if student and check_password_hash(student.password,password):
#             access_token = create_access_token(identity=student.id)
#             return {'access_token':access_token}, 200
#         return {'message': 'Invalid credentials'},401
    
class StudentLogin(Resource):
    def post(self):  
        data = request.get_json()
        email = data['email']
        password = data['password']
        
        student = Student.query.filter_by(email=email).first()
        # Check if both email and password are provided
        if student and check_password_hash(student.password, password):
            access_token = create_access_token(identity=student.id)
            # Include student details in the response
            student_details = {
                'id': student.id,
                'name': student.name,
                'email': student.email,
                'registrationNo':student.registrationNo,
                'gender':student.gender,
                'department':student.department,
                'semester':student.semester,
                'number':student.number,

  

                # Add more details as needed
            }
            return {'access_token': access_token, 'student': student_details}, 200
        return {'message': 'Invalid credentials'}, 401


class TeacherLogin(Resource):
    def post(self):  
        data = request.get_json()
        email = data['email']
        password =data['password']
        
        teacher = Teacher.query.filter_by(email=email).first()
        #Check if both email and password are provided
        if teacher and check_password_hash(teacher.password, password):
            access_token = create_access_token(identity=teacher.id)
            return {'access_token':access_token}, 200
        return {'message': 'Invalid credentials'},401
  
  


api.add_resource(StudentLogin,'/student_login')   
api.add_resource(TeacherRegistration,'/teacher_register')
api.add_resource(TeacherLogin,'/teacher_login')


# @app.route('/add_students', methods=['GET', 'POST'])
# def add_students():
#     if request.method == 'POST':
#         # Access form data using request.form.get()
#         name = request.form.get('name')
#         password = request.form.get('password')
#         email = request.form.get('email')
#         registrationNo = request.form.get('registrationNo')
#         gender = request.form.get('gender')
#         department = request.form.get('department')
#         technology = request.form.get('technology')
#         semester = request.form.get('semester')
#         number = request.form.get('number')

#         # Check if email and registration number exist and are not empty
#         if not email or not registrationNo:
#             flash('Email and Registration Number are required!', 'error')
#         elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
#             flash('Invalid email address!', 'error')
#         elif not all([name, password, gender, department, technology, semester, number]):
#             flash('Please fill out all fields!', 'error')
#         else:
#             # Check if email and registration number already exist
#             student_exists = Student.query.filter(
#                 db.or_(Student.email == email, Student.registrationNo == registrationNo)
#             ).first()
#             if student_exists:
#                 flash('Email or Registration Number already exists!', 'error')
#             else:
#                 # Create a new Student object
#                 new_student = Student(name=name, email=email, password=password, registrationNo=registrationNo, gender=gender, department=department, technology=technology, semester=semester, number=number)

#                 # Add the new student to the database session
#                 db.session.add(new_student)

#                 try:
#                     # Commit the session to persist changes
#                     db.session.commit()
#                     flash('Student has been successfully registered!', 'success')
#                 except Exception as e:
#                     db.session.rollback()
#                     flash('Error occurred while registering student. Please try again.', 'error')

#     return render_template('add_students.html')
  








# @app.route('/login_student', methods=['GET', 'POST'])
# # def login_student():
# #     message = ''
# #     if request.method == 'POST':
# #         email = request.form['email']
# #         password = request.form['password']
# #         print(email)
# #         print(password)
# #         if email == '' or password == '':
# #             message = 'Please enter email and password !'
# #         else:
# #             user = User.query.filter_by(email=email).first()
# #             print(user)
# #             if user is None:
# #                 message = 'Please enter correct email / password !'
# #             else:
                
# #                 #  if not bcrypt.check_password_hash(user.password, password):
# #                 #     message = 'Please enter correct email and password !'
# #                 #  else:    
# #                     session['loggedin'] = True
# #                     session['userid'] = user.id
# #                     session['name'] = user.name
# #                     session['email'] = user.email
# #                     message = 'Logged in successfully !'           


# def login_student():
#     if request.method == 'POST':
#         email = request.form.get('email')
#         password = request.form.get('password')

#         # Check if both email and password are provided
#         if not email or not password:
#             return jsonify({'message': 'Please provide email and password!'}), 400

#         # Query the database for the student with the provided email
#         student = Student.query.filter_by(email=email).first()

#         # Check if the student exists and the password matches
#         if student and student.password == password:
#             # Return success message and student details
#             return jsonify({
#                 'message': 'Login successful!',
#                 'student': {
#                     'id': student.id,
#                     'name': student.name,
#                     'email': student.email
#                     # Add other student details as needed
#                 }
#             }), 200
#         else:
#             # Return error message for incorrect credentials
#             return jsonify({'message': 'Invalid email or password!'}), 401

if __name__ == '__main__':
    app.run(debug=True)
