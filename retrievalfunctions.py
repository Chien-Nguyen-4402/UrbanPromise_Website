'''Functions to retrieve data from the database'''
# retrievalFunctions.py
# Author: Lois and Chien
#

import sys
import sqlalchemy
from sqlalchemy import insert, delete, select
from sqlalchemy import MetaData, Table
from datetime import datetime
import os

DATABASE_URL = os.getenv('DATABASE_URL')
DATABASE_URL =  DATABASE_URL.replace('postgres://', 'postgresql://')
engine = sqlalchemy.create_engine(DATABASE_URL, echo=True)
#----------------TUTOR INTERFACE-------------------------
#-------My Calendar--------------------

def write_availability(tutor_id_input, time_slot_input,
                       course_id_input, tutor_expertise_input):
    # Add new tutor availability into tutor_availability given
    # the specified input
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL, echo = True)
        with engine.connect() as connection:
            transaction = connection.begin()
            tutor_availability = sqlalchemy.Table('tutor_availability',
                sqlalchemy.MetaData(), autoload_with = engine)
            stmt = insert(tutor_availability).values(tutor_id = tutor_id_input,
                                            time_slot = time_slot_input,
                                            course_id = course_id_input,
                                            tutor_expertise = tutor_expertise_input)
            connection.execute(stmt)
            connection.begin
            transaction.commit()
            return True
    except Exception as exception:
        #transaction.rollback()
        print("Error in write_availability", file = sys.stderr)
        print(exception, file = sys.stderr)
        sys.exit(1)

def view_my_availability(tutor_id):
    # Given the tutor_id, retrieve the tutor's time slots and courses
    # taught at each time slot
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL, echo = True)
        with engine.connect() as connection:
            tutor_availability = sqlalchemy.Table('tutor_availability',
                sqlalchemy.MetaData(), autoload_with = engine)
            course_offerings = sqlalchemy.Table('course_offerings',
                sqlalchemy.MetaData(), autoload_with = engine)
            stmt = select(tutor_availability.c.time_slot,
                        course_offerings.c.course_name).where(
                        tutor_availability.c.tutor_id == tutor_id,
                        tutor_availability.c.course_id == course_offerings.c.course_id)
            result = connection.execute(stmt).fetchall()
            return result
    except Exception as exception:
        print("Error in view_my_availability", file = sys.stderr)
        print(exception, file = sys.stderr)
        sys.exit(1)

def check_tutor_availability(tutor_id_input, time_slot_input):
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL, echo = True)
        with engine.connect() as connection:
            tutor_availability = sqlalchemy.Table('tutor_availability',
                sqlalchemy.MetaData(), autoload_with = engine)
            stmt = select(tutor_availability.c.time_slot,).where(
                        tutor_availability.c.tutor_id == tutor_id_input,
                        tutor_availability.c.time_slot == time_slot_input)
            result = connection.execute(stmt).fetchall()
            if not result:
                return False
            else:
                return True
    except Exception as exception:
        print("Error in view_my_availability", file = sys.stderr)
        print(exception, file = sys.stderr)
        sys.exit(1)

def view_tutor_expertise(tutor_id, time_slot):
    # Given the tutor_id and a specific time_slot, get the tutor's
    # expertise for the couse taught at that time slot
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL, echo = True)
        with engine.connect() as connection:
            #transaction = connection.begin()
            tutor_availability = sqlalchemy.Table('tutor_availability',
                sqlalchemy.MetaData(), autoload_with = engine)
            stmt = select(tutor_availability.c.tutor_expertise).where(
                        tutor_availability.c.tutor_id == tutor_id,
                        tutor_availability.c.time_slot == time_slot)
            result = connection.execute(stmt).fetchall()
            #transaction.commit()
            return result
    except Exception as exception:
        print("Error in view_tutor_expertise", file = sys.stderr)
        print(exception, file = sys.stderr)
        sys.exit(1)

def view_student_reqs(tutor_email):
    # Give the tutor_id, return all students requesting to join this
    # tutor's class
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL, echo = True)

        with engine.connect() as connection:
            #transaction = connection.begin()

            student_info = sqlalchemy.Table('student_info',
                sqlalchemy.MetaData(), autoload_with = engine)
            tutors_info = sqlalchemy.Table('tutors_info',
                sqlalchemy.MetaData(), autoload_with = engine)
            course_offerings = sqlalchemy.Table('course_offerings',
                sqlalchemy.MetaData(), autoload_with = engine)
            student_enrollment_request = sqlalchemy.Table('student_enrollment_request',
                sqlalchemy.MetaData(), autoload_with = engine)
            tutor_id = connection.execute(select(tutors_info.c.tutor_id).where(tutors_info.c.tutor_email == tutor_email)).fetchall()[0][0]
            print(tutor_id,'sdfsd')
            stmt = select(student_info.c.student_name,
                        student_info.c.student_email,
                        course_offerings.c.course_name,
                        student_enrollment_request.c.time_slot,student_info.c.student_id,
                        course_offerings.c.course_id,student_enrollment_request.c.tutor_id).where(
                        student_enrollment_request.c.tutor_id == tutor_id,
                        student_info.c.student_id == student_enrollment_request.c.student_id,
                        course_offerings.c.course_id == student_enrollment_request.c.course_id)
            result = connection.execute(stmt).fetchall()
            #transaction.commit()
            return result
    except Exception as exception:
        print("Error in view_student_reqs", file = sys.stderr)
        print(exception, file = sys.stderr)
        sys.exit(1)

def check_student_duplicate_enrollment_request(student_id_input, course_id_input, time_slot_input, tutor_id_input):
    # View all requests to remove tutoring sessions from all tutors
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL, echo = True)
        with engine.connect() as connection:
            student_enrollment_request = sqlalchemy.Table('student_enrollment_request',
                sqlalchemy.MetaData(), autoload_with = engine)
            stmt = select(student_enrollment_request.c.student_id,
                          student_enrollment_request.c.course_id,
                          student_enrollment_request.c.time_slot,
                          student_enrollment_request.c.tutor_id).where(
                        student_enrollment_request.c.student_id == student_id_input,
                        student_enrollment_request.c.course_id == course_id_input,
                        student_enrollment_request.c.time_slot == time_slot_input,
                        student_enrollment_request.c.tutor_id == tutor_id_input
                        )
            # stmt = select(tutor_teaching_request)
            result = connection.execute(stmt).fetchall()
            if not result:
                return False
            else:
                return True
    except Exception as ex:
        print('Error in check_student_duplicate_enrollment_request', file=sys.stderr)
        print(ex,file=sys.stderr)
        sys.exit(1)

def check_tutor_duplicate_teach_request(course_id_input, time_slot_input, tutor_id_input):
    # View all requests to remove tutoring sessions from all tutors
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL, echo = True)
        with engine.connect() as connection:
            tutor_teach = sqlalchemy.Table('tutor_teaching_request',
                sqlalchemy.MetaData(), autoload_with = engine)
            stmt_select = select(sqlalchemy.exists().where(sqlalchemy.and_(
            tutor_teach.c.course_id == course_id_input,
            tutor_teach.c.tutor_id == tutor_id_input,
            tutor_teach.c.time_slot == time_slot_input)))
            result = connection.execute(stmt_select).fetchall()
            return result[0][0]
    except Exception as ex:
        print('Error in check_tutor_teach_dup', file=sys.stderr)
        print(ex,file=sys.stderr)
        sys.exit(1)
###### PLEASE DO NOT REMOVE THIS COMMENTED OUT PART IN CASE WE NEED IT FOR STRETCH GOALS ######

def check_table_tutor_id(table,tutor_id):
    engine = sqlalchemy.create_engine(DATABASE_URL, echo = True)
    try:
        with engine.connect() as connection:
            stmt_select = select(sqlalchemy.exists().where(sqlalchemy.and_(table.c.tutor_id == tutor_id)))
            result = connection.execute(stmt_select).fetchall()
            print('resf4',result[0][0])
            return result[0][0]
    except Exception as exception:
        print("Error in check_table_tutor_id", file = sys.stderr)
        print(exception, file = sys.stderr)

def remove_table_tutor_id(table, tutor_id):
    engine = sqlalchemy.create_engine(DATABASE_URL, echo = True)
    with engine.connect() as connection:
        transaction = connection.begin()
        stmt_delete = ''
        print('----------------------------------------------------')
        print(tutor_id)
        print('---------------------------------------------------')
        print(type(tutor_id))
        #if check_table_tutor_id(engine, table,tutor_email):
        stmt_delete = delete(table).where(
        table.c.tutor_id == tutor_id)
        connection.execute(stmt_delete)
        transaction.commit()
    engine.dispose

def remove_table_student_id(table, student_id):
    engine = sqlalchemy.create_engine(DATABASE_URL, echo = True)
    with engine.connect() as connection:
        transaction = connection.begin()
        stmt_delete = ''
        #if check_table_tutor_id(engine, table,tutor_email):
        print('----------------------------------------------------')
        print(student_id)
        print('---------------------------------------------------')
        stmt_delete = delete(table).where(
        table.c.student_id == student_id)
        connection.execute(stmt_delete)
        transaction.commit()
    engine.dispose



#-------Tutor Student Request Page-------
def accept_student_req(student_id_input, course_id_input,
                       time_slot_input,tutor_id_input):
    # Let the tutor to accept a student request
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL, echo = True)
        with engine.connect() as connection:
            transaction = connection.begin()

            student_tutors = sqlalchemy.Table('student_tutors',
                sqlalchemy.MetaData(), autoload_with = engine)
            student_enrollment_request = sqlalchemy.Table('student_enrollment_request',
                sqlalchemy.MetaData(), autoload_with = engine)
        # Insert a new row in student_tutors
            stmt_insert = insert(student_tutors).values(student_id = student_id_input,
                                            course_id = course_id_input,
                                            tutor_id = tutor_id_input,course_time = time_slot_input)
            connection.execute(stmt_insert)
#             #connection.commit()
        # Delete the request from student_enrollment_request
            stmt_delete = delete(student_enrollment_request).where(
                student_enrollment_request.c.student_id == student_id_input,
                student_enrollment_request.c.course_id == course_id_input,
                student_enrollment_request.c.time_slot == time_slot_input,
                student_enrollment_request.c.tutor_id == tutor_id_input)
            connection.execute(stmt_delete)
            # connection.commit()
            transaction.commit()
        return True
    except Exception as exception:
        print("Error in accept_student_req", file = sys.stderr)
        print(exception, file = sys.stderr)
        sys.exit(1)

def reject_student_req(student_id_input, course_id_input,
                       time_slot_input, tutor_id_input):
    try:
        # Delete the request from student_enrollment_request
        engine = sqlalchemy.create_engine(DATABASE_URL, echo = True)
        with engine.connect() as connection:
            transaction = connection.begin()

            student_enrollment_request = sqlalchemy.Table('student_enrollment_request',
                sqlalchemy.MetaData(), autoload_with = engine)
            stmt_delete = delete(student_enrollment_request).where(
                student_enrollment_request.c.student_id == student_id_input,
                student_enrollment_request.c.course_id == course_id_input,
                student_enrollment_request.c.time_slot == time_slot_input,
                student_enrollment_request.c.tutor_id == tutor_id_input)
            connection.execute(stmt_delete)
            # connection.commit()
            transaction.commit()
        return True
    except Exception as exception:
        print("Error in reject_student_req", file = sys.stderr)
        print(exception, file = sys.stderr)
        sys.exit(1)

# #-------------STUDENT INTERFACE--------------------------

# #-------Available Tutor Sessions---------

def view_tutors_availability():
    # Return all availabilities of all tutors
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL, echo = True)
        with engine.connect() as connection:
            #transaction = connection.begin()
            tutor_availability = sqlalchemy.Table('tutor_availability',
                sqlalchemy.MetaData(), autoload_with = engine)
            stmt = select(tutor_availability).where()
            result = connection.execute(stmt).fetchall()
            #transaction.commit()
            return result
    except Exception as ex:
        print('Error in view_tutors_availability', file=sys.stderr)
        print(ex, file=sys.stderr)
        sys.exit(1)

def view_tutors_availability_one(id_input):
    # Return all availabilities of all tutors
    # id = get_id
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL, echo = True)
        with engine.connect() as connection:
            #transaction = connection.begin()
            tutor_availability = sqlalchemy.Table('tutor_availability',
                sqlalchemy.MetaData(), autoload_with = engine)
            stmt = select(tutor_availability).where(tutor_availability.c.tutor_id == id_input)
            result = connection.execute(stmt).fetchall()
            #transaction.commit()
            return result
    except Exception as ex:
        print('Error in view_tutors_availability', file=sys.stderr)
        print(ex, file=sys.stderr)
        sys.exit(1)

# #-----------Appointment Sign-up----------

def write_student_reqs(student_id_input, course_id_input,
                       time_slot_input, tutor_id_input):
    # Add a new request to student_enrollment_request
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL, echo = True)
        with engine.connect() as connection:
            transaction = connection.begin()
            student_enrollment_request = sqlalchemy.Table('student_enrollment_request',
                sqlalchemy.MetaData(), autoload_with = engine)
            stmt = insert(student_enrollment_request).values(student_id = student_id_input,
                                                course_id = course_id_input,
                                                time_slot = time_slot_input,
                                                tutor_id = tutor_id_input)
            connection.execute(stmt)
            # connection.commit()
            transaction.commit()
            return True
    except Exception as ex:
        print('Error in write_student_reqs', file=sys.stderr)
        print(ex, file=sys.stderr)
        # sys.exit(1)
        return False

def new_course(course_name,course_id):
    # Add a new request to student_enrollment_request
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL, echo = True)
        with engine.connect() as connection:
            transaction = connection.begin()
            courses = sqlalchemy.Table('course_offerings',
                sqlalchemy.MetaData(), autoload_with = engine)

            stmt = insert(courses).values(course_id = course_id,
                                                course_name = course_name)
            connection.execute(stmt)
            # connection.commit()
            transaction.commit()
            return True
    except Exception as ex:
        print('Error in new_course', file=sys.stderr)
        print(ex, file=sys.stderr)
        # sys.exit(1)
        return False

# #----------My Tutors-----------------

def view_student_tutors(student_id):
    # Returns the list of all tutors a student has
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL, echo = True)
        with engine.connect() as connection:
            # #transaction = connection.begin()
            student_tutors = sqlalchemy.Table('student_tutors',
                sqlalchemy.MetaData(), autoload_with = engine)
            tutors_info = sqlalchemy.Table('tutors_info',
                sqlalchemy.MetaData(), autoload_with = engine)
            course_offerings = sqlalchemy.Table('course_offerings',
                sqlalchemy.MetaData(), autoload_with = engine)

            # Getting the list of tutors and course_id of courses
            # each tutor teach
            stmt0 = select(student_tutors.c.tutor_id,
                        student_tutors.c.course_id,student_tutors.c.course_time).where(
                        student_tutors.c.student_id == student_id)
            prelim_list = connection.execute(stmt0).fetchall()

            list_of_tutors = []

            # Getting the name and email of each tutor given their id,
            # and getting each course name given their course_id
            for row in prelim_list:
                tutor_id = int(row[0])
                course_id = int(row[1])
                course_time = row[2]
                stmt1 = select(tutors_info.c.tutor_name,
                        tutors_info.c.tutor_email).where(
                        tutors_info.c.tutor_id == tutor_id)
                stmt2 = select(course_offerings.c.course_name).where(
                        course_offerings.c.course_id == course_id)
                tutor = connection.execute(stmt1).fetchall()
                course_name = connection.execute(stmt2).fetchall()
                new_element = [tutor[0][0], tutor[0][1], course_name[0][0],course_time]
                list_of_tutors.append(new_element)
                # #transaction.commit()
            return list_of_tutors
    except Exception as ex:
        print('Error in view_student_tutors', file=sys.stderr)
        print(ex, file=sys.stderr)
        sys.exit(1)

def course_ids():
# Removes a tutor from a student's list of tutor
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL)
        with engine.connect() as connection:
            courses = sqlalchemy.Table('course_offerings',
                sqlalchemy.MetaData(), autoload_with = engine)
            # Get the id of a tutor given their tutor_id
            stmt_select = select(sqlalchemy.distinct(courses.c.course_id))

            # stmt_delete = delete(student_tutors).where(sqlalchemy.func.split_part(student_tutors.c.course_time,'_',1) == day_input)
            result = connection.execute(stmt_select).fetchall()
            return result
    except Exception as ex:
        print('Error in course_ids',file=sys.stderr)
        print(ex,file=sys.stderr)
        sys.exit(1)


def remove_student_tutor(student_id_input, course_id_input, tutor_email_input):
    # Removes a tutor from a student's list of tutor
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL, echo = True)
        with engine.connect() as connection:
            tutors_info = sqlalchemy.Table('tutors_info',
                sqlalchemy.MetaData(), autoload_with = engine)
            student_tutors = sqlalchemy.Table('student_tutors',
                sqlalchemy.MetaData(), autoload_with = engine)
            # Get the id of a tutor given their tutor_id
            stmt_select = select(tutors_info.c.tutor_id).where(
                tutors_info.c.tutor_email == tutor_email_input)
            result = connection.execute(stmt_select).fetchall()
            tutor_id_input = int(result[0][0])
            # Delete the row with teh given student_id_input,
            # course_id_input, and tutor_id_input
            stmt_delete = delete(student_tutors).where(
                student_tutors.c.student_id == student_id_input,
                student_tutors.c.course_id == course_id_input,
                student_tutors.c.tutor_id == tutor_id_input)
            connection.execute(stmt_delete)
            connection.commit()
            return True
    except Exception as ex:
        print('Error in remove_student_tutor',file=sys.stderr)
        print(ex,file=sys.stderr)
        sys.exit(1)


def matches_day(day_input):
    # Removes a tutor from a student's list of tutor
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL)
        with engine.connect() as connection:
            student_tutors = sqlalchemy.Table('student_tutors',
                sqlalchemy.MetaData(), autoload_with = engine)
            # Get the id of a tutor given their tutor_id
            stmt_select = select(student_tutors).where(sqlalchemy.func.split_part(student_tutors.c.course_time,'_',1) == day_input)

            # stmt_delete = delete(student_tutors).where(sqlalchemy.func.split_part(student_tutors.c.course_time,'_',1) == day_input)
            result = connection.execute(stmt_select).fetchall()
            return result
    except Exception as ex:
        print('Error in matches_day',file=sys.stderr)
        print(ex,file=sys.stderr)
        sys.exit(1)

def delete_day(day_input):
    # Removes a tutor from a student's list of tutor
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL)
        with engine.connect() as connection:
            student_tutors = sqlalchemy.Table('student_tutors',
                sqlalchemy.MetaData(), autoload_with = engine)
            # Get the id of a tutor given their tutor_id
            # stmt_select = select(student_tutors).where(sqlalchemy.func.split_part(student_tutors.c.course_time,'_',1) == day_input)

            stmt_delete = delete(student_tutors).where(sqlalchemy.func.split_part(student_tutors.c.course_time,'_',1) == day_input)
            connection.execute(stmt_delete)
            connection.commit()
            # print(result)
            # return result
            return "DB Updated"
    except Exception as ex:
        print('Error in delete_day',file=sys.stderr)
        print(ex,file=sys.stderr)
        return None
        # sys.exit(1)

# #-------------ADMIN INTERFACE----------------------------
def view_admins(admin_email_input):
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL, echo = True)
        with engine.connect() as connection:
            admins = sqlalchemy.Table('admins',
                sqlalchemy.MetaData(), autoload_with = engine)
            stmt = select(admins).where(admins.c.admin_email != admin_email_input).order_by(sqlalchemy.func.split_part(admins.c.admin_name,'_',2))
            result = connection.execute(stmt).fetchall()
            return result
    except Exception as ex:
        print('Error in admins', file=sys.stderr)
        print(ex,file=sys.stderr)
        sys.exit(1)

# #----------Tutor Request--------------

def view_tutor_reqs():
    # View all teaching requests from all tutors
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL, echo = True)
        with engine.connect() as connection:
            tutors_info = sqlalchemy.Table('tutors_info',
                sqlalchemy.MetaData(), autoload_with = engine)
            course_offerings = sqlalchemy.Table('course_offerings',
                sqlalchemy.MetaData(), autoload_with = engine)
            tutor_teaching_request = sqlalchemy.Table('tutor_teaching_request',
                sqlalchemy.MetaData(), autoload_with = engine)
            stmt = select(tutors_info.c.tutor_name, tutors_info.c.tutor_email,
                        tutor_teaching_request.c.time_slot,course_offerings.c.course_name,tutor_teaching_request.c.tutor_id,tutor_teaching_request.c.course_id,tutor_teaching_request.c.time_slot).where(
                        tutors_info.c.tutor_id == tutor_teaching_request.c.tutor_id,
                        course_offerings.c.course_id == tutor_teaching_request.c.course_id,
                        )
            # stmt = select(tutor_teaching_request)
            result = connection.execute(stmt).fetchall()
            return result
    except Exception as ex:
        print('Error in view_tutor_reqs', file=sys.stderr)
        print(ex,file=sys.stderr)
        sys.exit(1)

def view_tutor_remove_reqs():
    # View all requests to remove tutoring sessions from all tutors
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL, echo = True)
        with engine.connect() as connection:
            tutors_info = sqlalchemy.Table('tutors_info',
                sqlalchemy.MetaData(), autoload_with = engine)
            course_offerings = sqlalchemy.Table('course_offerings',
                sqlalchemy.MetaData(), autoload_with = engine)
            tutor_deteaching_request = sqlalchemy.Table('tutor_deteaching_request',
                sqlalchemy.MetaData(), autoload_with = engine)
            stmt = select(tutors_info.c.tutor_name, tutors_info.c.tutor_email,
                        tutor_deteaching_request.c.time_slot,course_offerings.c.course_name,
                        tutor_deteaching_request.c.tutor_id,tutor_deteaching_request.c.course_id,
                        tutor_deteaching_request.c.time_slot).where(
                        tutors_info.c.tutor_id == tutor_deteaching_request.c.tutor_id,
                        course_offerings.c.course_id == tutor_deteaching_request.c.course_id,
                        )
            # stmt = select(tutor_teaching_request)
            result = connection.execute(stmt).fetchall()
            return result
    except Exception as ex:
        print('Error in view_tutor_remove_reqs', file=sys.stderr)
        print(ex,file=sys.stderr)
        sys.exit(1)

def add_tutor_reqs(tutor_id_input, time_slot_input, course_id_input):
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL, echo = True)
        with engine.connect() as connection:
            transaction = connection.begin()
            tutor_teaching_request = sqlalchemy.Table('tutor_teaching_request',
                sqlalchemy.MetaData(), autoload_with = engine)
            stmt = insert(tutor_teaching_request).values(tutor_id = tutor_id_input,
                                            time_slot = time_slot_input,
                                            course_id = course_id_input)
            connection.execute(stmt)
            connection.begin
            transaction.commit()
            return True
    except Exception as exception:
        #transaction.rollback()
        print("Error in add_tutor_request", file = sys.stderr)
        print(exception, file = sys.stderr)
        sys.exit(1)

def add_tutor_remove_request(tutor_id_input, time_slot_input, course_id_input):
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL, echo = True)
        with engine.connect() as connection:
            transaction = connection.begin()
            tutor_deteaching_request = sqlalchemy.Table('tutor_deteaching_request',
                sqlalchemy.MetaData(), autoload_with = engine)
            stmt = insert(tutor_deteaching_request).values(tutor_id = tutor_id_input,
                                            time_slot = time_slot_input,
                                            course_id = course_id_input)
            connection.execute(stmt)
            connection.begin
            transaction.commit()
            return True
    except Exception as exception:
        #transaction.rollback()
        print("Error in add_tutor_remove_request", file = sys.stderr)
        print(exception, file = sys.stderr)
        sys.exit(1)

def check_tutor_duplicate_remove_request(tutor_id_input, time_slot_input, course_id_input):
    # View all requests to remove tutoring sessions from all tutors
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL, echo = True)
        with engine.connect() as connection:
            tutor_deteaching_request = sqlalchemy.Table('tutor_deteaching_request',
                sqlalchemy.MetaData(), autoload_with = engine)
            stmt = select(tutor_deteaching_request.c.tutor_id,
                          tutor_deteaching_request.c.time_slot,
                          tutor_deteaching_request.c.course_id).where(
                        tutor_deteaching_request.c.tutor_id == tutor_id_input,
                        tutor_deteaching_request.c.time_slot == time_slot_input,
                        tutor_deteaching_request.c.course_id == course_id_input
                        )
            # stmt = select(tutor_teaching_request)
            result = connection.execute(stmt).fetchall()
            if not result:
                return False
            else:
                return True
    except Exception as ex:
        print('Error in check_tutor_duplicate_remove_request', file=sys.stderr)
        print(ex,file=sys.stderr)
        sys.exit(1)

def accept_tutor_reqs(tutor_id_input, course_id_input,
                      time_slot_input, tutor_expertise_input):
    # Accept a tutor's teaching request given the specificed query,
    # adds it to tutor_availability and deletes it from tutor_teaching_request
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL)
        with engine.connect() as connection:
            transaction = connection.begin()
            # tutors_info = sqlalchemy.Table('tutors_info',
            #     sqlalchemy.MetaData(), autoload_with = engine)
            # course_offerings = sqlalchemy.Table('course_offerings',
            #     sqlalchemy.MetaData(), autoload_with = engine)
            tutor_availability = sqlalchemy.Table('tutor_availability',
                sqlalchemy.MetaData(), autoload_with = engine)
            # print('gets_avail')
            tutor_teaching_request = sqlalchemy.Table('tutor_teaching_request',
                sqlalchemy.MetaData(), autoload_with = engine)
            print('get_reqs')
            stmt_insert = insert(tutor_availability).values(
                tutor_id = tutor_id_input,
                time_slot = time_slot_input,
                course_id = course_id_input,
                tutor_expertise = tutor_expertise_input)
            connection.execute(stmt_insert)
            #connection.commit()
            # Remove the request from tutor_teaching_request
            # print('did_insert')
            stmt_delete = delete(tutor_teaching_request).where(
                tutor_teaching_request.c.tutor_id == tutor_id_input,
                tutor_teaching_request.c.time_slot == time_slot_input,
                tutor_teaching_request.c.course_id == course_id_input)
            connection.execute(stmt_delete)
            # connection.commit()
            transaction.commit()
            return True
    except Exception as ex:
        print('Error in accept_tutor_reqs', file=sys.stderr)
        print(ex, file=sys.stderr)
        sys.exit(1)

def accept_tutor_remove_reqs(tutor_id_input, course_id_input,
                      time_slot_input, tutor_expertise_input):
    # Accept a tutor's teaching request to remove a session in the schedule,
    # removes it from tutor_availability and deletes it from tutor_deteaching_request
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL)
        with engine.connect() as connection:
            transaction = connection.begin()
            tutor_availability = sqlalchemy.Table('tutor_availability',
                sqlalchemy.MetaData(), autoload_with = engine)
            tutor_deteaching_request = sqlalchemy.Table('tutor_deteaching_request',
                sqlalchemy.MetaData(), autoload_with = engine)
            stmt_delete_1 = delete(tutor_availability).where(
                tutor_availability.c.tutor_id == tutor_id_input,
                tutor_availability.c.time_slot == time_slot_input,
                tutor_availability.c.course_id == course_id_input,
                tutor_availability.c.tutor_expertise == tutor_expertise_input)
            connection.execute(stmt_delete_1)

            stmt_delete_2 = delete(tutor_deteaching_request).where(
                tutor_deteaching_request.c.tutor_id == tutor_id_input,
                tutor_deteaching_request.c.time_slot == time_slot_input,
                tutor_deteaching_request.c.course_id == course_id_input)
            connection.execute(stmt_delete_2)

            transaction.commit()
            return True
    except Exception as ex:
        print('Error in accept_tutor_remove_reqs', file=sys.stderr)
        print(ex, file=sys.stderr)
        sys.exit(1)

def reject_tutor_reqs(tutor_id_input, course_id_input, time_slot_input):
    # Deletes a request from tutor's teaching request
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL)
        with engine.connect() as connection:
            transaction = connection.begin()
            tutor_teaching_request = sqlalchemy.Table('tutor_teaching_request',
                sqlalchemy.MetaData(), autoload_with = engine)
            stmt_delete = delete(tutor_teaching_request).where(
                tutor_teaching_request.c.tutor_id == tutor_id_input,
                tutor_teaching_request.c.time_slot == time_slot_input,
                tutor_teaching_request.c.course_id == course_id_input)
            connection.execute(stmt_delete)
            transaction.commit()
            # connection.commit()
            return True
    except Exception as ex:
        print('Error in reject_tutor_reqs', file=sys.stderr)
        print(ex, file=sys.stderr)
        sys.exit(1)

def reject_tutor_remove_reqs(tutor_id_input, course_id_input, time_slot_input):
    # Deletes a request from tutor's_deteaching_request table
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL)
        with engine.connect() as connection:
            transaction = connection.begin()
            tutor_deteaching_request = sqlalchemy.Table('tutor_deteaching_request',
                sqlalchemy.MetaData(), autoload_with = engine)
            stmt_delete = delete(tutor_deteaching_request).where(
                tutor_deteaching_request.c.tutor_id == tutor_id_input,
                tutor_deteaching_request.c.time_slot == time_slot_input,
                tutor_deteaching_request.c.course_id == course_id_input)
            connection.execute(stmt_delete)
            transaction.commit()
            return True
    except Exception as ex:
        print('Error in reject_tutor_remove_reqs', file=sys.stderr)
        print(ex, file=sys.stderr)
        sys.exit(1)

# #----------Current Tutors-------------
def tutor_avail_check(dia,tid):
    # Returns the list of all tutors
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL, echo = True)
        with engine.connect() as connection:
            # course_offerings = sqlalchemy.Table('course_offerings',
            #     sqlalchemy.MetaData(), autoload_with = engine)
            tutor_availability = sqlalchemy.Table('tutor_availability',
                sqlalchemy.MetaData(), autoload_with = engine)
            stmt_select = select(tutor_availability.c.time_slot).where(sqlalchemy.and_(sqlalchemy.func.split_part(tutor_availability.c.time_slot,'_',1) == dia,tutor_availability.c.tutor_id == tid))

            # Create the select statement with the join
            result = connection.execute(stmt_select).fetchall()
            return result
    except Exception as exception:
        print("Error in view_all_tutors", file = sys.stderr)
        print(exception, file = sys.stderr)
        sys.exit(1)


def view_all_tutors():
    # Returns the list of all tutors
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL, echo = True)
        with engine.connect() as connection:
            tutors_info = sqlalchemy.Table('tutors_info',
                sqlalchemy.MetaData(), autoload_with = engine)
            # course_offerings = sqlalchemy.Table('course_offerings',
            #     sqlalchemy.MetaData(), autoload_with = engine)
            tutor_availability = sqlalchemy.Table('tutor_availability',
                sqlalchemy.MetaData(), autoload_with = engine)
            # stmt_select_tutor = select(tutors_info).where()
            join_condition = tutor_availability.c.tutor_id == tutors_info.c.tutor_id

            # Create the join
            join_obj = sqlalchemy.join(tutor_availability,tutors_info, join_condition)

# Create the select statement with the join
            stmt_select = select(tutors_info.c.tutor_name,tutors_info.c.tutor_email,tutor_availability.c.time_slot,tutor_availability.c.tutor_expertise,tutor_availability.c.course_id,tutor_availability.c.tutor_id).select_from(join_obj).order_by(
            tutor_availability.c.tutor_expertise, tutors_info.c.tutor_name
            ).order_by(sqlalchemy.func.split_part(tutors_info.c.tutor_name,'_',2))
            result = connection.execute(stmt_select).fetchall()
            return result
    except Exception as exception:
        print("Error in view_all_tutors", file = sys.stderr)
        print(exception, file = sys.stderr)
        sys.exit(1)

def view_all_tutors1():
    # Returns the list of all tutors
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL, echo = True)
        with engine.connect() as connection:
            tutors_info = sqlalchemy.Table('tutors_info',
                sqlalchemy.MetaData(), autoload_with = engine)
# Create the select statement with the join
            stmt_select = select(tutors_info)


            result = connection.execute(stmt_select).fetchall()
            return result
    except Exception as exception:
        print("Error in view_all_tutors", file = sys.stderr)
        print(exception, file = sys.stderr)
        sys.exit(1)

# #--------View Students---------------
def view_all_students():
    # Returns a list of all students ordered by last name for the admin to view
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL, echo = True)
        with engine.connect() as connection:
            student_info = sqlalchemy.Table('student_info',
                sqlalchemy.MetaData(), autoload_with = engine)
            stmt_select = select(student_info.c.student_name,
                                student_info.c.student_email).order_by(sqlalchemy.func.split_part(student_info.c.student_name,'_',2))
            result = connection.execute(stmt_select).fetchall()
            return result
    except Exception as exception:
        print("Error in view_all_students", file = sys.stderr)
        print(exception, file = sys.stderr)

def view_students(tutor_id_input):
    # Returns the list of all students of a tutor, given the tutor_id
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL)
        with engine.connect() as connection:
            student_info = sqlalchemy.Table('student_info',
                sqlalchemy.MetaData(), autoload_with = engine)
            student_tutors = sqlalchemy.Table('student_tutors',
                sqlalchemy.MetaData(), autoload_with = engine)
            course_offerings = sqlalchemy.Table('course_offerings',
                sqlalchemy.MetaData(), autoload_with = engine)
            # tutors_courses = sqlalchemy.Table('tutors_courses',
            #     sqlalchemy.MetaData(), autoload_with = engine)
            stmt_select = select(student_info.c.student_name,
                                student_info.c.student_email,
                                course_offerings.c.course_name,student_tutors.c.course_time).where(
                                student_tutors.c.tutor_id == tutor_id_input,
                                student_tutors.c.student_id == student_info.c.student_id,
                                student_tutors.c.course_id == course_offerings.c.course_id,
                                ).distinct()
            result = connection.execute(stmt_select).fetchall()
            return result
    except Exception as exception:
        print("Error in view_students", file = sys.stderr)
        print(exception, file = sys.stderr)

def student_email_from_id(id):
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL, echo = True)
        with engine.connect() as connection:
            student_info = sqlalchemy.Table('student_info',
                sqlalchemy.MetaData(), autoload_with = engine)
            stmt_select = select(student_info.c.student_email).where(student_info.c.student_id == id)
            result = connection.execute(stmt_select).fetchall()
            return result[0][0]
    except Exception as exception:
        print("Error in student_email_from_id", file = sys.stderr)
        print(exception, file = sys.stderr)


def tutor_name_from_id(id):
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL, echo = True)
        with engine.connect() as connection:
            tutor_info = sqlalchemy.Table('tutors_info',
                sqlalchemy.MetaData(), autoload_with = engine)
            stmt_select = select(tutor_info.c.tutor_name).where(tutor_info.c.tutor_id == id)
            result = connection.execute(stmt_select).fetchall()
            return result[0][0]
    except Exception as exception:
        print("Error in tutor_name_from_id", file = sys.stderr)
        print(exception, file = sys.stderr)

def student_id_from_email(student_email):
#     if student_email.count('\n') == 0:
#         student_email += '\n'
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL, echo = True)
        with engine.connect() as connection:
            student_info = sqlalchemy.Table('student_info',
                sqlalchemy.MetaData(), autoload_with = engine)
            stmt_select = select(student_info.c.student_id).where(student_info.c.student_email == student_email)
            result = connection.execute(stmt_select).fetchall()
            return result[0][0]
    except Exception as exception:
        print("Error in student_id_from_email", file = sys.stderr)
        print(exception, file = sys.stderr)

def tutor_id_from_email(tutor_email):
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL, echo = True)
        with engine.connect() as connection:
            tutors_info = sqlalchemy.Table('tutors_info',
                sqlalchemy.MetaData(), autoload_with = engine)
            stmt_select = select(tutors_info.c.tutor_id).where(tutors_info.c.tutor_email == tutor_email)
            result = connection.execute(stmt_select).fetchall()
            return result[0][0]
    except Exception as exception:
        print("Error in tutor_id_from_email", file = sys.stderr)
        print(exception, file = sys.stderr)
        sys.exit(1)

def course_id_from_course_name(course_name):
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL, echo = True)
        with engine.connect() as connection:
            course_offerings = sqlalchemy.Table('course_offerings',
                sqlalchemy.MetaData(), autoload_with = engine)
            stmt_select = select(course_offerings.c.course_id).where(course_offerings.c.course_name == course_name)
            result = connection.execute(stmt_select).fetchall()
            print('got here')
            if not result:
                return "Can't find course"
            else:
                return result[0][0]

    except Exception as exception:
        print("Error in course_id_from_course_name", file = sys.stderr)
        print(exception, file = sys.stderr)
        sys.exit(1)

def course_name_from_course_id(course_id):
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL, echo = True)
        with engine.connect() as connection:
            course_offerings = sqlalchemy.Table('course_offerings',
                sqlalchemy.MetaData(), autoload_with = engine)
            stmt_select = select(course_offerings.c.course_name).where(course_offerings.c.course_id == course_id)
            result = connection.execute(stmt_select).fetchall()
            if not result:
                return "Can't find course"
            else:
                return result[0][0]

    except Exception as exception:
        print("Error in course_name_from_course_id", file = sys.stderr)
        print(exception, file = sys.stderr)
        sys.exit(1)

def view_all_courses():
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL, echo = True)
        with engine.connect() as connection:
            course_offerings = sqlalchemy.Table('course_offerings',
                sqlalchemy.MetaData(), autoload_with = engine)
            stmt_select = select(course_offerings.c.course_name)
            result = connection.execute(stmt_select).fetchall()
            return result
    except Exception as exception:
        print("Error in view_all_courses", file = sys.stderr)
        print(exception, file = sys.stderr)

def tutor_email_from_id(id):
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL, echo = True)
        with engine.connect() as connection:
            tutor_info = sqlalchemy.Table('tutors_info',
                sqlalchemy.MetaData(), autoload_with = engine)
            stmt_select = select(tutor_info.c.tutor_email).where(tutor_info.c.tutor_id == id)
            result = connection.execute(stmt_select).fetchall()
            return result[0][0]
    except Exception as exception:
        print("Error in tutor_email_from_id", file = sys.stderr)
        print(exception, file = sys.stderr)


def check_dup(student_id_input,course_id_input,tutor_id_input,course_time_input):
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL, echo = True)
        with engine.connect() as connection:
            student_tutors = sqlalchemy.Table('student_tutors',sqlalchemy.MetaData(), autoload_with = engine)
            stmt_select = select(sqlalchemy.exists().where(sqlalchemy.and_(student_tutors.c.student_id == student_id_input,student_tutors.c.course_id == course_id_input,student_tutors.c.tutor_id == tutor_id_input,student_tutors.c.course_time == course_time_input)))
            result = connection.execute(stmt_select).fetchall()
            # print('resf4',result[0][0])
            return result[0][0]
    except Exception as exception:
        print("Error in check_dup", file = sys.stderr)
        print(exception, file = sys.stderr)

def check_studentinfo_dup(email):
        try:
            engine = sqlalchemy.create_engine(DATABASE_URL, echo = True)
            with engine.connect() as connection:
                student_info = sqlalchemy.Table('student_info',sqlalchemy.MetaData(), autoload_with = engine)
                stmt_select = select(sqlalchemy.exists().where(sqlalchemy.and_(student_info.c.student_email == email)))
                result = connection.execute(stmt_select).fetchall()
                # print('resf4',result[0][0])
                return result[0][0]
        except Exception as exception:
            print("Error in check_studentinfo_dup", file = sys.stderr)
            print(exception, file = sys.stderr)

def check_tutorinfo_dup(email):
        try:
            engine = sqlalchemy.create_engine(DATABASE_URL, echo = True)
            with engine.connect() as connection:
                tutors_info = sqlalchemy.Table('tutors_info',sqlalchemy.MetaData(), autoload_with = engine)
                stmt_select = select(sqlalchemy.exists().where(sqlalchemy.and_(tutors_info.c.tutor_email == email)))
                result = connection.execute(stmt_select).fetchall()
                # print('resf4',result[0][0])
                return result[0][0]
        except Exception as exception:
            print("error in check_tutorinfo_dup", file = sys.stderr)
            print(exception, file = sys.stderr)

def check_admininfo_dup(email):
        try:
            engine = sqlalchemy.create_engine(DATABASE_URL, echo = True)
            with engine.connect() as connection:
                admins = sqlalchemy.Table('admins',sqlalchemy.MetaData(), autoload_with = engine)
                stmt_select = select(sqlalchemy.exists().where(sqlalchemy.and_(admins.c.admin_email == email)))
                result = connection.execute(stmt_select).fetchall()
                # print('resf4',result[0][0])
                return result[0][0]
        except Exception as exception:
            print("error in check_admininfo_dup", file = sys.stderr)
            print(exception, file = sys.stderr)


def get_emails(num):
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL, echo = True)
        with engine.connect() as connection:
            if num == '2':
                tutors_info = sqlalchemy.Table('tutors_info',sqlalchemy.MetaData(), autoload_with = engine)
                stmt_select = select(tutors_info.c.tutor_id)
            elif num == '3':
                student_info = sqlalchemy.Table('student_info',sqlalchemy.MetaData(), autoload_with = engine)
                stmt_select = select(student_info.c.student_id)
            result = connection.execute(stmt_select).fetchall()
            # print('resf4',result[0][0])
            return result
    except Exception as exception:
        print("error in get_emails", file = sys.stderr)
        print(exception, file = sys.stderr)

def main():
    # Testing write_availability
    # tutor_id = 1000
    # time_slot = "1400-1600"
    # course_id = 1
    # tutor_expertise = "Proficient"
    # write_availability(tutor_id, time_slot, course_id, tutor_expertise)

    # # Testing view_my_availability
    # list_of_availability = view_my_availability(4192)
    # print("-----------------------------")
    # for row in list_of_availability:
    #     print(row)
    # print("------------------------------")

    #Testing view_tutor_expertise
    # result = view_tutor_expertise(4709, "0800-1015")
    # print("-----------------------")
    # for row in result:
    #     print(row)
    # print("-----------------------")

    # Testing view_student_enrollment_request
    # result = view_student_reqs(2743)
    # print("-----------------------")
    # for row in result:
    #     print(row)
    # print("-----------------------")

    # Testing accept_student_request
    # accept_student_req(2099202486, 15507, "1900-2100", 1702)

    # Testing reject_student_request
    # reject_student_req(2035807497, 84646, "0300-0430", 4348)

    # Testing view_tutors_availability
    # result = view_tutors_availability()
    # print("---------------------")
    # for row in result:
    #     print(row)
    # print("---------------------")

    # Testing write_student_reqs
    # write_student_reqs(2035807497, 84646, "0300-0430", 4348)
    # write_student_reqs(2099202486, 15507, "1900-2100", 1702)

    #Testing view_student_tutors
    # result = view_student_tutors(2099202486)
    # print("-------------------")
    # for row in result:
    #     print(row)
    # print("--------------------")

    # Testing remove_student_tutors
    # remove_student_tutor(2099202486, 15507, "linda@gmail.com")

    # Testing view_tutor_reqs
    # result = view_tutor_reqs(7085)
    # print("--------------------")
    # for row in result:
    #     print(row)
    # print("--------------------")

    # Testing accept_tutor_reqs
    # accept_tutor_reqs("evelyn@gmail.com", "AP,PSYCH", "0900 - 1200", "Proficient")
    # accept_tutor_reqs("richard@gmail.com", "AP,US,HISTORY",
    #                   "0700-0815", "Proficent")

    # Testing reject_tutor_reqs
    # reject_tutor_reqs("belle@gmail.com", "ANATOMY", "1000-1100")

    # Testing view_all_tutors
    # result = view_all_tutors()
    # print("---------------------")
    # for row in result:
    #     print(row)
    # print("---------------------")

    # Test view_students
    # result = view_students(2680)
    # print("----------------")
    # for row in result:
    #     print(row)
    # print("----------------")

    #Test course_id_from_course_name
    # result = course_id_from_course_name("AP_CALC_BC")
    # print("------------------------------------")
    # print(len(result))
    # print(result[0][0])
    # print("-------------------------------------")

    #Test course_name_from_course_id
    # course_name = course_name_from_course_id(62810)
    # print(course_name.replace('\n','_'))
    # print(course_name == "AP_CALC_BC")

    #Test view_may_availability
    # result1 = view_my_availability(6906)
    # print("--------------------------------------")
    # for row in result1:
    #     print(row[1].replace('\n','_'))
    # print("--------------------------------------")
    # result2= view_my_availability(5344)
    # print("--------------------------------------")
    # for row in result2:
    #     print(row[1].replace('\n','_'))
    # print("--------------------------------------------")
    # result3 = view_my_availability(5977)
    # print("--------------------------------------------")
    # for row in result3:
    #     print(row[1].replace('\n','_'))
    # print("--------------------------------------------")

    #Test check_tutor_duplicate_remove_request
    # result = check_tutor_duplicate_remove_request(1562, "Tuesday 2-2:30 PM", 55580)
    # print("----------------------------------------")
    # print(result)
    # print("-----------------------------------------")
    # result = check_tutor_duplicate_remove_request(5117, "Tuesday 2-2:30 PM", 55580)
    # print("----------------------------------------")
    # print(result)
    # print("-----------------------------------------")
    # result = check_tutor_duplicate_remove_request(2056, "Thursday_1:30_PM-4:00_PM", 39550)
    # print("----------------------------------------")
    # print(result)
    # print("-----------------------------------------")

    # Test check_student_duplicate_enrollment_request
    # Should be true, false, true
    result = check_student_duplicate_enrollment_request(2030493268, 80328, "Wednesday_8:00_AM-9:00_AM", 6336)
    print("----------------------------------------")
    print(result)
    print("----------------------------------------")
    result = check_student_duplicate_enrollment_request(2015389244, 46100, "Friday_4:00_PM-6:00_PM", 6336)
    print("----------------------------------------")
    print(result)
    print("----------------------------------------")
    result = check_student_duplicate_enrollment_request(2051621795, 46099, "Tuesday_11:00_AM-12:00_PM", 5186)
    print("----------------------------------------")
    print(result)
    print("----------------------------------------")

if __name__ == '__main__':
    main()
