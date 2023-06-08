#-----------------------------------------------------------------
# Lois I. Omotara
# populate_alpha.py
#-----------------------------------------------------------------
import sqlalchemy
import os
import sqlalchemy.orm as so
import alpha_database as ad
import sys

DATABASE_URL_ = os.getenv('DATABASE_URL')
DATABASE_URL_ =  DATABASE_URL_.replace('postgres://', 'postgresql://')

def create_course(line):
    id = line[1]
    name = line[2]
    return ad.course_offerings(course_id=id, course_name=name)
def create_tutor_availability(line):
    id = line[1]
    time = line[2]
    cid = line[3]
    expertise = line[4]
    return ad.tutor_availability(tutor_id = id,
    time_slot = time, course_id=cid, tutor_expertise=expertise)
def create_student_request(line):
    id = line[1]
    cid= line[2]
    time = line[3]
    tid = line[4]
    return ad.student_enrollment_request(student_id=id,course_id=cid,time_slot=time,tutor_id=tid)
def create_tutor_request(line):
    id = line[1]
    time = line[2]
    cid = line[3]
    return ad.tutor_teaching_request(tutor_id=id, time_slot=time,course_id=cid)
def create_admin(line):
    name = line[1]
    email = line[2].replace('\n','')
    return ad.admin(admin_name=name,admin_email=email)
def create_student(line):
    id = line[1]
    name = line[2]
    email = line[3].replace('\n','')
    return ad.student_info(student_id=id, student_name=name, student_email=email)
def create_student_tutor(line):
    id = line[1]
    cid = line[2]
    tid = line[3]
    ctime = line[4]
    return ad.student_tutors(student_id=id,course_id=cid,tutor_id=tid,course_time = ctime)
def create_tutor(line):
    id = line[1]
    name = line[2]
    email = line[3].replace('\n','')
    return ad.tutors_info(tutor_id=id,tutor_name=name,tutor_email=email)
def create_tutors_course(line):
    id = line[1]
    cid = line[2]
    cname = line[3]
    ctime = line[4]
    return ad.tutors_courses(tutor_id=id, course_id=cid,course_name=cname,course_time =ctime)

def main():
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL_)
        with so.Session(engine) as session:
            with open('auto_mock_data.txt','r') as mock_data:
                mock_lines = mock_data.readlines()
                for line in mock_lines:
                    line_split = line.split(' ')
                    request = None
                    if line_split[0] == "course_offerings":
                        request = create_course(line_split)
                    elif line_split[0] == 'tutor_availability':
                        request = create_tutor_availability(line_split)
                    elif line_split[0] == 'student_enrollment_request':
                        request = create_student_request(line_split)
                    elif line_split[0] == 'tutor_teaching_request':
                        request = create_tutor_request(line_split)
                    elif line_split[0] == "administrator":
                        request = create_admin(line_split)
                    elif line_split[0] == "student_info":
                        request = create_student(line_split)
                    elif line_split[0] == "student_tutors":
                        request = create_student_tutor(line_split)
                    elif line_split[0] == "tutors_info":
                        request = create_tutor(line_split)
                    elif line_split[0] == 'tutors_courses':
                        request = create_tutors_course(line_split)
                    else:
                        print('-----------------------------')
                        print(line_split[0])
                    session.add(request)
                    session.commit()
        engine.dispose()
    except Exception as ex:
        print(ex,file=sys.stderr)
        sys.exit(1)


if __name__=='__main__':
    main()
