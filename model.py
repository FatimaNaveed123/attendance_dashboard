from flask_sqlalchemy import SQLAlchemy
          
db = SQLAlchemy()
          
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True, unique=True)
    email = db.Column(db.String(50), index=True, unique=True)
    password = db.Column(db.String(60), index=True, unique=True)
    

class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True)
    email = db.Column(db.String(50), index=True, unique=True)
    password = db.Column(db.String(60), index=True)
    registrationNo = db.Column(db.String(20), index=True,unique=True)
    gender = db.Column(db.String(10), index=True)
    department = db.Column(db.String(30), index=True)
    technology = db.Column(db.String(20), index=True)
    semester = db.Column(db.String(5), index=True)
    number = db.Column(db.String(20), index=True)


class Teacher(db.Model):
    __tablename__ = "teachers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True)
    email = db.Column(db.String(50), index=True, unique=True)
    password = db.Column(db.String(60), index=True)
    registrationNo = db.Column(db.String(20), index=True,unique=True)
    gender = db.Column(db.String(10), index=True)
    department = db.Column(db.String(30), index=True)
    number = db.Column(db.String(20), index=True)