#----------------------------------------------------------------------
# Author: Lois I Omotara
# database4.py
#----------------------------------------------------------------------

import sqlalchemy.ext.declarative
import sqlalchemy

Base = sqlalchemy.ext.declarative.declarative_base()

class course_offerings(Base):
    __tablename__='course_offerings'
    course_id = sqlalchemy.Column(sqlalchemy.Integer,primary_key=True)
    course_name = sqlalchemy.Column(sqlalchemy.String)

class tutor_availability(Base):
    __tablename__='tutor_availability'
    tutor_id = sqlalchemy.Column(sqlalchemy.Integer,primary_key=True)
    time_slot = sqlalchemy.Column(sqlalchemy.String,primary_key=True)
    course_id = sqlalchemy.Column(sqlalchemy.Integer,primary_key=True)
    tutor_expertise = sqlalchemy.Column(sqlalchemy.String)

class student_enrollment_request(Base):
    __tablename__='student_enrollment_request'
    student_id = sqlalchemy.Column(sqlalchemy.Integer,primary_key=True)
    course_id = sqlalchemy.Column(sqlalchemy.Integer,primary_key=True)
    time_slot = sqlalchemy.Column(sqlalchemy.String,primary_key=True)
    tutor_id = sqlalchemy.Column(sqlalchemy.Integer,primary_key=True)

class tutor_teaching_request(Base):
    __tablename__='tutor_teaching_request'
    tutor_id = sqlalchemy.Column(sqlalchemy.Integer,primary_key=True)
    time_slot = sqlalchemy.Column(sqlalchemy.String,primary_key=True)
    course_id = sqlalchemy.Column(sqlalchemy.Integer,primary_key=True)

class tutor_deteaching_request(Base):
    __tablename__='tutor_deteaching_request'
    tutor_id = sqlalchemy.Column(sqlalchemy.Integer,primary_key=True)
    time_slot = sqlalchemy.Column(sqlalchemy.String,primary_key=True)
    course_id = sqlalchemy.Column(sqlalchemy.Integer,primary_key=True)


class admin(Base):
    __tablename__='admins'
    admin_name = sqlalchemy.Column(sqlalchemy.String,primary_key=True)
    admin_email = sqlalchemy.Column(sqlalchemy.String,primary_key=True)

class student_info(Base):
    __tablename__='student_info'
    student_id = sqlalchemy.Column(sqlalchemy.Integer,primary_key=True)
    student_name =sqlalchemy.Column(sqlalchemy.String)
    student_email = sqlalchemy.Column(sqlalchemy.String)

class student_tutors(Base):
    __tablename__='student_tutors'
    student_id = sqlalchemy.Column(sqlalchemy.Integer,primary_key=True)
    course_id = sqlalchemy.Column(sqlalchemy.Integer,primary_key=True)
    tutor_id = sqlalchemy.Column(sqlalchemy.Integer,primary_key=True)
    course_time = sqlalchemy.Column(sqlalchemy.String,primary_key=True)

class tutors_info(Base):
    __tablename__='tutors_info'
    tutor_id = sqlalchemy.Column(sqlalchemy.Integer,primary_key=True)
    tutor_name = sqlalchemy.Column(sqlalchemy.String)
    tutor_email = sqlalchemy.Column(sqlalchemy.String)

class tutors_courses(Base):
    __tablename__='tutors_courses'
    tutor_id = sqlalchemy.Column(sqlalchemy.Integer,primary_key=True)
    course_id = sqlalchemy.Column(sqlalchemy.Integer,primary_key=True)
    course_name = sqlalchemy.Column(sqlalchemy.String,primary_key=True)
    course_time = sqlalchemy.Column(sqlalchemy.String,primary_key=True)
