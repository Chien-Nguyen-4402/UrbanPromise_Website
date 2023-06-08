#----------------------------------------------------------------------
# Author: Lois I Omotara
# database4.py
#----------------------------------------------------------------------

import sqlalchemy.ext.declarative
import sqlalchemy

Base = sqlalchemy.ext.declarative.declarative_base()

class Course_Offerings(Base):
    __tablename__='course_offerings'
    course_id = sqlalchemy.Column(sqlalchemy.Integer,primary_key=True)
    course_name = sqlalchemy.Column(sqlalchemy.String)

class Tutor_Availability(Base):
    __tablename__='tutor_availability'
    tutor_id = sqlalchemy.Column(sqlalchemy.Integer,primary_key=True)
    time_slot = sqlalchemy.Column(sqlalchemy.String)
    course_id = sqlalchemy.Column(sqlalchemy.Integer)
    tutor_expertise = sqlalchemy.Column(sqlalchemy.String)

class Student_Request(Base):
    __tablename__='student_enrollment_request'
    student_id = sqlalchemy.Column(sqlalchemy.Integer,primary_key=True)
    course_id = sqlalchemy.Column(sqlalchemy.Integer)
    time_slot = sqlalchemy.Column(sqlalchemy.String)
    tutor_id = sqlalchemy.Column(sqlalchemy.Integer)
class Tutor_Request(Base):
    __tablename__='tutor_request'
    tutor_id = sqlalchemy.Column(sqlalchemy.Integer,primary_key=True)
    time_slot = sqlalchemy.Column(sqlalchemy.String)
    course_id = sqlalchemy.Column(sqlalchemy.Integer)

class Admin(Base):
    __tablename__='admins'
    admin_name = sqlalchemy.Column(sqlalchemy.String,primary_key=True)
    admin_email = sqlalchemy.Column(sqlalchemy.String)

class Student_Info(Base):
    __tablename__='student_info'
    student_id = sqlalchemy.Column(sqlalchemy.Integer,primary_key=True)
    student_name =sqlalchemy.Column(sqlalchemy.String)
    student_email = sqlalchemy.Column(sqlalchemy.String)

class Student_Tutors(Base):
    __tablename__='student_tutors'
    student_id = sqlalchemy.Column(sqlalchemy.Integer,primary_key=True)
    course_id = sqlalchemy.Column(sqlalchemy.Integer)
    tutor_id = sqlalchemy.Column(sqlalchemy.Integer)

class Tutors_Info(Base):
    __tablename__='tutors_info'
    tutor_id = sqlalchemy.Column(sqlalchemy.Integer,primary_key=True)
    tutor_name = sqlalchemy.Column(sqlalchemy.String)
    tutor_email = sqlalchemy.Column(sqlalchemy.String)

class Tutors_Courses(Base):
    __tablename__='tutors_courses'
    tutor_id = sqlalchemy.Column(sqlalchemy.Integer,primary_key=True)
    course_id = sqlalchemy.Column(sqlalchemy.Integer)
    course_name = sqlalchemy.Column(sqlalchemy.String)
