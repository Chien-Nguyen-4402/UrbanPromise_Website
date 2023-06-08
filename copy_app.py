#TEMPLATE
#!/usr/bin/env python




#-----------------------------------------------------------------------
# code is based off of templates.py


#need starttime and endtime field in tutor_availability
#need to
#protect against dupiclate requests in tutor_teach
#-----------------------------------------------------------------------
import html
import sys
import flask
import sqlalchemy
from sqlalchemy import select, delete
import psycopg2
import random
import re
import retrievalfunctions
import auth
import os
import datetime
import schedule
import threading
import time
import sqlalchemy.orm as so
import alpha_database as ad
import email_notif as email
import ast
import securitymeasures as sm
import flask_wtf.csrf


# Create a thread for the function

#import template


app = flask.Flask(__name__, template_folder='.')
app.secret_key = os.getenv('APP_KEY')
flask_wtf.csrf.CSRFProtect(app)

DATABASE_URL = os.getenv('DATABASE_URL')
DATABASE_URL =  DATABASE_URL.replace('postgres://', 'postgresql://')

def db_update():
    try:
        today = ["Monday", "Tuesday",
                "Wednesday",
                "Thursday", "Friday",
                "Saturday", "Sunday"][(datetime.datetime.today() - datetime.timedelta(days = 1)).weekday()]

        print(retrievalfunctions.matches_day(today))
        print(retrievalfunctions.delete_day(today))
        print(retrievalfunctions.matches_day(today))
        # else:
        #     print('got to none')
    except Exception:
        return flask.redirect('/error')

schedule.every().day.at('02:00').do(db_update)

def thread_update():
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except Exception:
        return flask.redirect('/error')

background_thread = threading.Thread(target=thread_update)
# Start the thread
background_thread.start()

@app.errorhandler(flask_wtf.csrf.CSRFError)
def csrferror(error):
    html_code = flask.render_template('generalerror.html',type_error='400 error',reason=error)
    print(error)
    return flask.make_response(html_code)

@app.errorhandler(404)
def error404(error):
    html_code = flask.render_template('404error.html')
    print(error)
    return flask.make_response(html_code)

@app.errorhandler(500)
def error500(error):
    html_code = flask.render_template('generalerror.html',type_error='500 error',reason=error)
    print(error)
    return flask.make_response(html_code)

@app.route('/error',methods=['GET'])
def error():
    html_code = flask.render_template('404error.html')
    return flask.make_response(html_code)

@app.route('/header', methods=['GET'])
def header():
    try:
        html_code = flask.render_template('header.html')
        response = flask.make_response(html_code)
        return response
    except Exception:
        return flask.redirect('/error')



@app.route('/static/<path:filename>')
def static_file(filename):
    return app.send_static_file(filename)

@app.route('/adduser',methods = ['GET'])
def adduser():
    try:
        if sm.checkadmin():
            return flask.redirect('/')
        html_code = flask.render_template('register_user.html')
        response =  flask.make_response(html_code)
        return response
    except Exception:
        return flask.redirect('/error')

# @app.route('/addadmin', methods = ['GET'])
# def addadmin():
#     if sm.checkadmin():
#         return flask.redirect('/signin')
#     html_code = flask.render_template('register_admin.html')
#     response = flask.make_response(html_code)
#     return response

@app.route('/remove',methods = ['GET'])
def remove():
    try:
        if sm.checkadmin():
            return flask.redirect('/signin')
        html_code = flask.render_template('removeperson.html')
        response = flask.make_response(html_code)
        return response
    except Exception:
        return flask.redirect('/error')

@app.route('/handleremove', methods = ['POST'])
def handleremove():
    try:
        user_type = flask.request.form.get('type_user')
        email_address = flask.request.form.get('email')
        print("************************************************")
        print("Check point 1")
        print("************************************************")
        if user_type is None:
            flask.flash('user_type missing', 'error')
            return flask.redirect('/remove')
        if len(user_type.replace(' ','')) == 0:
            flask.flash('user_type missing', 'error')
            return flask.redirect('/remove')
        print("************************************************")
        print("Checkpoint 2")
        print("************************************************")
        if email_address is None:
            flask.flash('Email missing','error')
            return flask.redirect('/remove')
        if len(email_address.replace(' ','')) == 0:
            flask.flash('Email missing','error')
                    # print('should flash')
            return flask.redirect('/remove')
        try:
            engine = sqlalchemy.create_engine(DATABASE_URL, echo = True)
            with engine.connect() as connection:
                transaction = connection.begin()
                tutors_info = sqlalchemy.Table('tutors_info',
                    sqlalchemy.MetaData(), autoload_with = engine)
                tutor_courses  = sqlalchemy.Table('tutors_courses',
                    sqlalchemy.MetaData(), autoload_with = engine)
                tutor_avail = sqlalchemy.Table('tutor_availability',
                    sqlalchemy.MetaData(), autoload_with = engine)
                tutor_teach_reqs = sqlalchemy.Table('tutor_teaching_request',
                    sqlalchemy.MetaData(), autoload_with = engine)
                tutor_deteach_reqs = sqlalchemy.Table('tutor_deteaching_request',
                    sqlalchemy.MetaData(), autoload_with = engine)
                student_tutors = sqlalchemy.Table('student_tutors',
                    sqlalchemy.MetaData(), autoload_with = engine)
                student_enroll_reqs = sqlalchemy.Table('student_enrollment_request',
                    sqlalchemy.MetaData(), autoload_with = engine)
                student_info = sqlalchemy.Table('student_info',
                    sqlalchemy.MetaData(), autoload_with = engine)
                admin = sqlalchemy.Table('admins',
                    sqlalchemy.MetaData(), autoload_with = engine)
                stmt_delete = ''
                if user_type == '2':
                    print("************************************************")
                    print("Check point 3")
                    print("************************************************")
                    if retrievalfunctions.check_tutorinfo_dup(email_address) is False:
                        flask.flash('This email is not registered as a tutor','error')
                        return flask.redirect('/remove')
                    tutor_id = retrievalfunctions.tutor_id_from_email(email_address)
                    stmt_delete = delete(tutors_info).where(
                    tutors_info.c.tutor_email == email_address)
                    retrievalfunctions.remove_table_tutor_id(table=student_tutors, tutor_id=tutor_id)
                    retrievalfunctions.remove_table_tutor_id(table=tutor_courses, tutor_id=tutor_id)
                    retrievalfunctions.remove_table_tutor_id(table=tutor_avail,tutor_id=tutor_id)
                    retrievalfunctions.remove_table_tutor_id(table=tutor_teach_reqs, tutor_id=tutor_id)
                    retrievalfunctions.remove_table_tutor_id(table=tutor_deteach_reqs, tutor_id=tutor_id)


                elif user_type == '3':
                    if retrievalfunctions.check_studentinfo_dup(email_address) is False:
                        flask.flash('This email is not registered as a student','error')
                        return flask.redirect('/remove')
                    student_id = retrievalfunctions.student_id_from_email(email_address)
                    stmt_delete = delete(student_info).where(
                    student_info.c.student_email == email_address)
                    retrievalfunctions.remove_table_student_id(table=student_tutors,student_id=student_id)
                    retrievalfunctions.remove_table_student_id(table=student_enroll_reqs,student_id=student_id)
                elif user_type == '1':
                    if retrievalfunctions.check_admininfo_dup(email_address) is False:
                        flask.flash('This email is not registered as an admin','error')
                        return flask.redirect('/remove')
                    if email_address == auth.authenticate():
                        flask.flash('You cannot remove yourself')
                        return flask.redirect('/remove')
                    stmt_delete = delete(admin).where(
                    admin.c.admin_email == email_address)
                else:
                    flask.flash('No user type chosen','error')
                    return flask.redirect('/remove')
                connection.execute(stmt_delete)
                flask.flash('User successfully deleted','success')
                # connection.commit()
                transaction.commit()
            engine.dispose()
            print("**********************************************")
            print("user_type")
            print(user_type)
            print("**********************************************")
            print("**********************************************")
            print("email_address")
            print(email_address)
            print("**********************************************")
            subject = "Your UrbanPromise membership has been terminated"
            body = f"Your access to the UrbanPromise website has been terminated by admin."
            print("**********************************************")
            print(subject)
            print(body)
            print("**********************************************")
            email.send(body=body, subject=subject, email=email_address)
            return flask.redirect('/remove')
        except Exception as ex:
            print(ex, file=sys.stderr)
            flask.flash('Server Error has occured')
            return flask.redirect('/remove')
    except Exception as exception:
        print("************************************************")
        print(exception)
        print("************************************************")
        return flask.redirect('/error')

@app.route('/registeruser', methods=['POST'])
def handleregister():
    try:
        user_type = flask.request.form.get('type_user')
        name = flask.request.form.get('name')
        name = name.replace(' ','_').upper()
        email_address = flask.request.form.get('email')
        print('dsf,',name,'dfs',email_address)
        # print('len,',len(name.replace(' ','')))
        if len(name.replace(' ','')) == 0:
            flask.flash('Name missing', 'error')
            return flask.redirect('/adduser')
        if len(email_address.replace(' ','')) == 0:
            flask.flash('Email missing','error')
                    # print('should flash')
            return flask.redirect('/adduser')

        # id = flask.request.form.get('id')
        engine = sqlalchemy.create_engine(DATABASE_URL)
        try:
            with so.Session(engine) as session:
                request = ''
                if user_type == '1':
                    if retrievalfunctions.check_admininfo_dup(email_address):
                        flask.flash('This email is already registered as an admin','error')
                        print('should flash')
                        return flask.redirect('/adduser')
                    if retrievalfunctions.check_tutorinfo_dup(email_address):
                        flask.flash('This email is already registered as a tutor','error')
                        return flask.redirect('/adduser')
                    elif retrievalfunctions.check_studentinfo_dup(email_address):
                        flask.flash('This email is already registered as a student','error')
                        return flask.redirect('/adduser')
                    request = ad.admin(admin_name = name, admin_email = email_address)
                elif user_type == '2':
                    if retrievalfunctions.check_admininfo_dup(email_address):
                        flask.flash('This email is already registered as an admin','error')
                        print('should flash')
                        return flask.redirect('/adduser')
                    if retrievalfunctions.check_tutorinfo_dup(email_address):
                        flask.flash('This email is already registered as a tutor','error')
                        return flask.redirect('/adduser')
                    elif retrievalfunctions.check_studentinfo_dup(email_address):
                        flask.flash('This email is already registered as a student','error')
                        return flask.redirect('/adduser')
                    current_ids = [x[0] for x in retrievalfunctions.get_emails(user_type)]
                    id = random.sample(list(set (range (0,10000) ).symmetric_difference(set(current_ids))),1)[0]
                    request = ad.tutors_info(tutor_id=id, tutor_name = name, tutor_email = email_address)

                elif user_type == '3':
                    if retrievalfunctions.check_admininfo_dup(email_address):
                        flask.flash('This email is already registered as an admin','error')
                        print('should flash')
                        return flask.redirect('/adduser')
                    if retrievalfunctions.check_tutorinfo_dup(email_address):
                        flask.flash('This email is already registered as a tutor','error')
                        return flask.redirect('/adduser')
                    elif retrievalfunctions.check_studentinfo_dup(email_address):
                        flask.flash('This email is already registered as a student','error')
                        return flask.redirect('/adduser')
                    current_ids = [x[0] for x in retrievalfunctions.get_emails(user_type)]
                    id = random.sample(list(set (range (0,10000) ).symmetric_difference(set(current_ids))),1)[0]
                    request = ad.student_info(student_id = id, student_name=name, student_email = email_address)
                else:
                    flask.flash('No user type chosen','error')
                    return flask.redirect('/adduser')
                session.add(request)
                session.commit()
            engine.dispose()
            flask.flash('The user has been successfully registered', 'success')
            print("**********************************************")
            print("user_type")
            print(user_type)
            print("**********************************************")
            print("**********************************************")
            print("email_address")
            print(email_address)
            print("**********************************************")
            subject = "You are now an UrbanPromise member"
            body = f"You have been added as a member on the UrbanPromise website."
            print("**********************************************")
            print(subject)
            print(body)
            print("**********************************************")
            email.send(body=body, subject=subject, email=email_address)
            return flask.redirect('/adduser')
        except Exception as ex:
            print(ex,file=sys.stderr)
            return None
    except Exception:
        return flask.redirect('/error')

# @app.route('/registeradmin',methods = ['POST'])
# def registeradmin():
#     try:
#         name = flask.request.form.get('admin_name')
#         email = flask.request.form.get('admin_email')
#         engine = sqlalchemy.create_engine(DATABASE_URL)
#         with so.Session(engine) as session:
#             if retrievalfunctions.check_admininfo_dup(email):
#                 flask.flash('This email is already registered as an admin','error')
#                 print('should flash')
#                 return flask.redirect('/addadmin')
#             request = ad.admin(admin_name = name, admin_email = email)
#             session.add(request)
#             session.commit()
#         engine.dispose()
#         flask.flash('The admin has been successfully registered!', 'success')
#         return flask.redirect('/addadmin')
#     except Exception as ex:
#         print(ex,file=sys.stderr)
#         flask.flash('An error has occured!', 'error')
#         return flask.redirect('/addadmin')

@app.route('/markpresent', methods = ['POST'])
def markepresent():
    try:
        try:
            engine = sqlalchemy.create_engine(DATABASE_URL, echo = True)
            admin = sqlalchemy.Table('admins',
                        sqlalchemy.MetaData(), autoload_with = engine)
            with engine.connect() as connection:
                stmt_select_admin = select(admin.c.admin_email)
                admin_emails = [x[0].replace('\n','') for x in connection.execute(stmt_select_admin).fetchall()]
                for admin_email in admin_emails:
                    appointment = flask.request.form.get('time_slot')
                    appointment = ast.literal_eval(appointment)
                    print(type(appointment),'sdfsdf')
                    body = f"{appointment[0].title()} {appointment[1]} has been marked present for the appointment"
                    body += f" {appointment[2][:-1].replace('_',' ')} at {appointment[-1][:-1].replace('_',' ')}"
                    subject = 'Student Present'
                    print()
                    email.send(body=body,subject=subject,email=admin_email)
            flask.flash('Student marked as present','success')
            return flask.redirect('/tutor_students')
        except Exception as ex:
            print(ex,file=sys.stderr)
            flask.flash('Student has not been marked as present', 'error')
            return flask.redirect('/tutor_students')
    except Exception as ex:
        print('*****************************************')
        print(ex)
        print('****************************************')
        return flask.redirect('/error')


@app.route('/markabsent',methods = ['POST'])
def markabsent():
    try:
        try:
            engine = sqlalchemy.create_engine(DATABASE_URL, echo = True)
            admin = sqlalchemy.Table('admins',
                        sqlalchemy.MetaData(), autoload_with = engine)
            with engine.connect() as connection:
                stmt_select_admin = select(admin.c.admin_email)
                admin_emails = [x[0].replace('\n','') for x in connection.execute(stmt_select_admin).fetchall()]
                for admin_email in admin_emails:
                    appointment = flask.request.form.get('time_slot')
                    appointment = ast.literal_eval(appointment)
                    body = f"{appointment[0].title()} {appointment[1]} has been marked absent for the appointment"
                    body += f" {appointment[2][:-1].replace('_',' ')} at {appointment[-1][:-1].replace('_',' ')}"
                    subject = 'Student Absent'
                    email.send(body=body,subject=subject,email=admin_email)
            flask.flash('Student marked as absent','success')
            # current_tutor = flask.request.form.get('tutor_id')
            return flask.redirect('/tutor_students')
        except Exception as ex:
            print(ex,file=sys.stderr)
            flask.flash('Student has not been marked as absent', 'error')
            return flask.redirect('/tutor_students')
    except Exception as ex:
        print(ex)
        return flask.redirect('/error')


@app.route('/footer', methods=['GET'])
def footer():
    try:
        html_code = flask.render_template('footer.html')
        response = flask.make_response(html_code)
        return response
    except Exception:
        return flask.redirect('/error')

@app.route('/admin_teach', methods=['GET'])
def admin_teach():
    try:
        if sm.checkadmin():
            return flask.redirect('/signin')
        print(flask.session['email'],'emmmm')
        options = retrievalfunctions.view_tutor_reqs()
        #print('opts =',options)
        html_code = flask.render_template('admin_teach.html',options = options)
        response = flask.make_response(html_code)
        return response
    except Exception:
        return flask.redirect('/error')

@app.route('/admin_deteach', methods=['GET'])
def admin_deteach():
    try:
        if sm.checkadmin():
            return flask.redirect('/signin')
        # print(flask.session['email'],'emmmm')

        options = retrievalfunctions.view_tutor_remove_reqs()
        print("****************************************************")
        print("Requests to remove sessions")
        for row in options:
            print(row)
        print("****************************************************")
        #print('opts =',options)
        html_code = flask.render_template('admin_deteach.html',options = options)
        response = flask.make_response(html_code)
        return response
    except Exception:
        flask.redirect('/error')

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    try:
        html_code = flask.render_template('index.html')
        response = flask.make_response(html_code)
        return response
    except Exception:
        return flask.redirect('/error')


@app.route('/about', methods=['GET'])
def about():
    try:
        html_code = flask.render_template('about.html')
        response = flask.make_response(html_code)
        return response
    except Exception as ex:
        print('*******************************************')
        print(ex)
        print('*******************************************')
        return flask.redirect('/error')

@app.route('/aindex', methods=['GET'])
def aboutindex():
    try:
        html_code = flask.render_template('about_index.html')
        response = flask.make_response(html_code)
        return response
    except Exception as ex:
        print('*******************************************')
        print(ex)
        print('*******************************************')
        return flask.redirect('/error')


@app.route('/login/callback', methods=['GET'])
def callback():
    try:
        return auth.callback()
    except Exception as ex:
        print('*******************************************')
        print(ex)
        print('*******************************************')
        return flask.redirect('/error')

@app.route('/login', methods=['GET','POST'])
def login():
    try:
        return auth.login()
    except Exception as ex:
        print('*******************************************')
        print(ex)
        print('*******************************************')
        return flask.redirect('/error')

@app.route('/logout', methods=['GET','POST'])
def logout():
    try:
        return auth.logoutapp()
    except Exception:
        return flask.redirect('/error')

@app.route('/view_admins',methods = ['GET'])
def view_admins():
    try:
        if sm.checkadmin():
            return flask.redirect('/signin')
        admins = retrievalfunctions.view_admins(auth.authenticate())
        html_code = flask.render_template('view_admins.html',options = admins)
        response = flask.make_response(html_code)
        return response
    except Exception:
        return flask.redirect('/error')

@app.route('/admin_tutors',methods = ['GET'])
def admin_tutors():
    try:
        if sm.checkadmin():
            return flask.redirect('/signin')
        courses = retrievalfunctions.view_all_tutors1()
        html_code = flask.render_template('admin_tutors.html',courses=courses)
        response = flask.make_response(html_code)
        return response
    except Exception as ex :
        print('Exception in admin_tutors')
        print('****************************************************')
        print(ex)
        print('***************************************************')
        return flask.redirect('/error')

@app.route('/admin_students',methods = ['GET'])
def admin_students():
    try:
        if sm.checkadmin():
            return flask.redirect('/signin')
        courses = retrievalfunctions.view_all_students()
        html_code = flask.render_template('admin_students.html',courses=courses)
        response = flask.make_response(html_code)
        return response
    except Exception:
        return flask.redirect('/error')

@app.route('/signin', methods=['GET','POST'])
def signin():
    # username = auth.authenticate()
    username = flask.session['email']
    username = username.replace('\n','')

    try:
        engine = sqlalchemy.create_engine(DATABASE_URL, echo = True)
        tutors_info = sqlalchemy.Table('tutors_info',
                sqlalchemy.MetaData(), autoload_with = engine)
        student_info = sqlalchemy.Table('student_info',
                sqlalchemy.MetaData(), autoload_with = engine)
        admin = sqlalchemy.Table('admins',
                sqlalchemy.MetaData(), autoload_with = engine)
        with engine.connect() as connection:
            stmt_select_admin = select(admin.c.admin_email)

            admin_emails = [x[0].replace('\n','') for x in connection.execute(stmt_select_admin).fetchall()]
            if username in admin_emails:
#                 courses = retrievalfunctions.view_admins(username+'\n')
                courses = retrievalfunctions.view_admins(username)
                html_code = flask.render_template('admin.html',options=courses)
                response = flask.make_response(html_code)
                return response

            stmt_select_student = select(student_info.c.student_email)
            student_emails = [x[0].replace('\n','') for x in connection.execute(stmt_select_student).fetchall()]
            if username in student_emails:
#                 username1 = username + '\n'
                username = username.replace('\n','')
                stmt_select_student_id = select(student_info.c.student_id).where(
                    student_info.c.student_email == username)
                student_id = connection.execute(stmt_select_student_id).fetchall()[0][0]
                options = retrievalfunctions.view_student_tutors(student_id)
                html_code = flask.render_template('student.html', options = options)
                response = flask.make_response(html_code)
                return response
            stmt_select_tutor = select(tutors_info.c.tutor_email)
            tutor_emails = [x[0].replace('\n','') for x in connection.execute(stmt_select_tutor).fetchall()]

            if username in tutor_emails:
#                 username1 = username + '\n'

                stmt_select_tutor_id = select(tutors_info.c.tutor_id).where(
                    tutors_info.c.tutor_email == username)
#                 tutors_info.c.tutor_email == username1)
                tutor_id = connection.execute(stmt_select_tutor_id).fetchall()[0][0]
                options = retrievalfunctions.view_students(tutor_id)
                html_code = flask.render_template('tutor_students.html',options = options)
                html_code = html_code.replace("Students","My Students")
                response = flask.make_response(html_code)
                return response
            else:
                flask.flash('Your email is not registered, please contact an administrator', 'success')
                html_code = flask.render_template('index.html')
                response = flask.make_response(html_code)
                return response

    except Exception as exception:
        print("Error in login() of copy_app", file = sys.stderr)
        print(exception, file = sys.stderr)
        return flask.redirect('/error')


@app.route('/admin', methods=['GET'])
def admin():
    try:
        if sm.checkadmin():
            return flask.redirect('/signin')
        admins = retrievalfunctions.view_admins()
        html_code = flask.render_template('admin.html',options = admins)
        response = flask.make_response(html_code)
        return response
    except Exception:
        return flask.redirect('/error')

@app.route('/view_students', methods=['GET'])
def view_students():
    try:
        if sm.checkadmin():
            return flask.redirect('/signin')
        html_code = flask.render_template('admin.html')
        response = flask.make_response(html_code)
        return response
    except Exception:
        flask.redirect('/error')

@app.route("/admin_tutor_students", methods=['GET','POST'])
def admin_tutor_students():
    try:
        if sm.checkadmin():
            return flask.redirect('/signin')
        print(flask.request.form,'arf')
        post_id = flask.request.form['tutor_id']
        tutor_name = flask.request.form['tutor_name']
        print(flask.request.form)
        print(tutor_name,'dfadsf')
        options = retrievalfunctions.view_students(post_id)
        print(options,'opps')
        html_code = flask.render_template("admin_tutor_students.html",courses = options,name = tutor_name)
        response = flask.make_response(html_code)
        return response
    except Exception:
        return flask.redirect('/error')


@app.route("/admin_tutor_avail", methods=['GET','POST'])
def admin_tutor_avail():
    try:
        if sm.checkadmin():
            return flask.redirect('/signin')
        print(flask.request.form,'arf')
        post_id = flask.request.form['tutor_id']
        tutor_name = flask.request.form['tutor_name']
        print(flask.request.form)
        print(tutor_name,'dfadsf')
        options = retrievalfunctions.view_tutors_availability_one(post_id)
        print(options,'opps')
        html_code = flask.render_template("admin_tutor_avail.html",infos = options,name = tutor_name)
        response = flask.make_response(html_code)
        return response
    except Exception:
        return flask.redirect('/error')

@app.route("/tutor_students", methods=['GET','POST'])
def tutor_students():
    try:
        if sm.checktutor():
            return flask.redirect('/signin')
        #post_id = flask.request.form['tutor_id']
        post_id = retrievalfunctions.tutor_id_from_email(auth.authenticate())
        options = retrievalfunctions.view_students(post_id)
        html_code = flask.render_template("tutor_students.html",options = options)
        response = flask.make_response(html_code)
        return response
    except Exception:
        return flask.redirect('/error')

@app.route("/admin_accept", methods=['POST'])
def admin_accept():
    try:
        if sm.checkadmin():
            return flask.redirect('/signin')
        # return flask.redirect('/index')
        print('formmm',flask.request.form)
        tm,cn,ts,te = flask.request.form['tutor_id'],flask.request.form['course_id'],flask.request.form['time_slot'],flask.request.form['tutor_expertise']
        # options = retrievalfunctions.view_students(post_id)
        # print(tm,cn,ts,te,'dsfadsf')
        retrievalfunctions.accept_tutor_reqs(tutor_id_input = tm,course_id_input = cn,time_slot_input = ts,tutor_expertise_input = te)
        tutor_email = retrievalfunctions.tutor_email_from_id(tm)
        print("**********************************************")
        print("tutor_email")
        print(tutor_email)
        print("**********************************************")
        subject = "Request to add a tutoring session"
        body = f"Your request to add a tutoring session on {ts} has been accepted. Log into the UrbanPromise website to view your new schedule"
        print("**********************************************")
        print(subject)
        print(body)
        print("**********************************************")
        email.send(body=body, subject=subject, email=tutor_email)
        # options = retrievalfunctions.view_tutor_reqs()
        # html_code = flask.render_template('admin_teach.html',options = options)
        # response = flask.make_response(html_code)
        return flask.redirect('/admin_teach')
    except Exception:
        return flask.redirect('/error')

@app.route("/admin_deteach_accept", methods=['POST'])
def admin_deteach_accept():
    try:
        if sm.checkadmin():
            return flask.redirect('/signin')
        # return flask.redirect('/index')
        # print('formmm',flask.request.form)
        tm,cn,ts,te = flask.request.form['tutor_id'],flask.request.form['course_id'],flask.request.form['time_slot'],flask.request.form['tutor_expertise']
        # options = retrievalfunctions.view_students(post_id)
        # print(tm,cn,ts,te,'dsfadsf')
        retrievalfunctions.accept_tutor_remove_reqs(tutor_id_input = tm,course_id_input = cn,time_slot_input = ts,tutor_expertise_input = te)
        tutor_email = retrievalfunctions.tutor_email_from_id(tm)
        print("**********************************************")
        print("tutor_email")
        print(tutor_email)
        print("**********************************************")
        subject = "Request to remove a tutoring session"
        body = f"Your request to remove a tutoring session on {ts} has been accepted. Log into the UrbanPromise website to view your new schedule"
        print("**********************************************")
        print(subject)
        print(body)
        print("**********************************************")
        email.send(body=body, subject=subject, email=tutor_email)
        # options = retrievalfunctions.view_tutor_remove_reqs()
        # html_code = flask.render_template('admin_deteach.html',options = options)
        # response = flask.make_response(html_code)
        return flask.redirect('/admin_deteach')
    except Exception:
        return flask.redirect('/error')

@app.route("/admin_reject", methods=['POST'])
def admin_reject():
    try:
        if sm.checkadmin():
            return flask.redirect('/signin')
        print(flask.request.form,'forum')
        tm,cn,ts = flask.request.form['tutor_id'],flask.request.form['course_id'],flask.request.form['time_slot']
        # options = retrievalfunctions.view_students(post_id)
        retrievalfunctions.reject_tutor_reqs(tm,cn,ts)
        tutor_email = retrievalfunctions.tutor_email_from_id(tm)
        print("**********************************************")
        print("tutor_email")
        print(tutor_email)
        print("**********************************************")
        subject = "Request to add a tutoring session"
        body = f"Your request to add a tutoring session on {ts} has been rejected. Log into the UrbanPromise website to view your full schedule"
        print("**********************************************")
        print(subject)
        print(body)
        print("**********************************************")
        email.send(body=body, subject=subject, email=tutor_email)
        # options = retrievalfunctions.view_tutor_reqs()
        # html_code = flask.render_template('admin_teach.html',options = options)
        # response = flask.make_response(html_code)
        return flask.redirect('/admin_teach')
    except Exception:
        return flask.redirect('/error')

@app.route("/admin_deteach_reject", methods=['POST'])
def admin_deteach_reject():
    try:
        if sm.checkadmin():
            return flask.redirect('/signin')
        # print(flask.request.form,'forum')
        tm,cn,ts = flask.request.form['tutor_id'],flask.request.form['course_id'],flask.request.form['time_slot']
        # options = retrievalfunctions.view_students(post_id)
        retrievalfunctions.reject_tutor_remove_reqs(tm,cn,ts)
        tutor_email = retrievalfunctions.tutor_email_from_id(tm)
        print("**********************************************")
        print("tutor_email")
        print(tutor_email)
        print("**********************************************")
        subject = "Request to remove a tutoring session"
        body = f"Your request to remove a tutoring session on {ts} has been rejected. Log into the UrbanPromise website to view your full schedule"
        print("**********************************************")
        print(subject)
        print(body)
        print("**********************************************")
        email.send(body=body, subject=subject, email=tutor_email)
        # options = retrievalfunctions.view_tutor_remove_reqs()
        # html_code = flask.render_template('admin_deteach.html',options = options)
        # response = flask.make_response(html_code)
        return flask.redirect('/admin_deteach')
    except Exception:
        return flask.redirect('/error')

@app.route("/tutor_requests", methods=['GET'])
def tutor_requests():
    try:
        if sm.checktutor():
            return flask.redirect('/signin')
        reqs = retrievalfunctions.view_student_reqs(flask.session['email'])
        print(reqs,'dasfads')
        html_code = flask.render_template("tutor_requests.html",courses = reqs)
        response = flask.make_response(html_code)
        return response
    except Exception:
        return flask.redirect('/error')

@app.route("/tutor_accept", methods=['POST'])
def tutor_accept():
    try:
        if sm.checktutor():
            return flask.redirect('/signin')
        params = flask.request.form
        student_id,course_id,time_slot,tutor_id = params.get('student_id'),params.get('course_id'),params.get('time_slot'),params.get('tutor_id')
        retrievalfunctions.accept_student_req(student_id_input=student_id,
                                                    course_id_input=course_id,
                                                    time_slot_input=time_slot,
                                                    tutor_id_input=tutor_id)
        student_email = retrievalfunctions.student_email_from_id(student_id)
        subject = 'Your Appointment Request has been accepted'
        tutor_name = retrievalfunctions.tutor_name_from_id(tutor_id)
        body = '''You now have an appointment at '''+time_slot.replace('_',' ') +''' with the tutor '''+tutor_name.replace('_',' ')+'''

        You can contact them at this email: '''+auth.authenticate()
        email.send(subject=subject, body=body, email=student_email)
        return flask.redirect('/tutor_requests')
        # reqs = retrievalfunctions.view_student_reqs(auth.authenticate())
        # html_code = flask.render_template("tutor_requests.html",courses = reqs)
        # response = flask.make_response(html_code)
        # return response
    except Exception:
        return flask.redirect('/error')

@app.route("/tutor_reject", methods=['POST'])
def tutor_reject():
    try:
        if sm.checktutor():
            return flask.redirect('/signin')
        params = flask.request.form
        student_id,course_id,time_slot,tutor_id = params.get('student_id'),params.get('course_id'),params.get('time_slot'),params.get('tutor_id')
        retrievalfunctions.reject_student_req(student_id_input=student_id,
                                                    course_id_input=course_id,
                                                    time_slot_input=time_slot,
                                                    tutor_id_input=tutor_id)
        student_email = retrievalfunctions.student_email_from_id(student_id)
        subject = 'Your Appointment Request has been rejected'
        tutor_name = retrievalfunctions.tutor_name_from_id(tutor_id)
        body = '''Your appointment request for the '''+time_slot.replace('_',' ') +''' with the tutor '''+tutor_name.replace('_',' ') +'''
        has been rejected

        You can contact them at this email: '''+auth.authenticate()
        email.send(subject=subject, body=body, email=student_email)
        # reqs = retrievalfunctions.view_student_reqs(flask.session['email'])
        # html_code = flask.render_template("tutor_requests.html",courses = reqs)
        # response = flask.make_response(html_code)
        return flask.redirect('/tutor_requests')
    except Exception:
        return flask.redirect('/error')

def nearest_day(day):
    today = datetime.date.today()
    days_ahead = (7 - today.weekday() + ["Monday","Tuesday","Wednesday","Thursday","Friday", "Saturday", "Sunday"].index(day)) % 7

    nearest_date = today + datetime.timedelta(days=days_ahead)
    almost = nearest_date.strftime('%A %B %d' + ('th' if 11<=nearest_date.day<=13 else {1:'st', 2:'nd', 3:'rd'}.get(nearest_date.day % 10, 'th')) + ', %Y')
    for i in [1,2,3,4,5,6,7,8,9]:
        almost = almost.replace(f'0{i}t',f'{i}t')
        almost = almost.replace(f'0{i}n',f'{i}n')
        almost = almost.replace(f'0{i}r',f'{i}r')
        almost = almost.replace(f'0{i}s',f'{i}s')
    return almost

@app.route('/requesttutor', methods=['GET'])
def request_tutor():
    try:
        print("************************************************")
        print("Checkpoint 1")
        print("************************************************")
        if sm.checkstudent():
            return flask.redirect('/signin')
        courses = retrievalfunctions.view_all_tutors()

        days = [nearest_day(x[2].replace(' ','_').split('_')[0]) for x in courses]
        # print(list(courses[0]) + [days[0]])
        # fo
        cs = [tuple(list(course) + [day]) for course,day in zip(courses,days)]
        # print(cs)
        # print([t + (new_element,) for t, new_element in zip(courses, days)])
        print("************************************************")
        print("Checkpoint 2")
        print("************************************************")
        html_code = flask.render_template('request_tutor.html',courses = cs)
        print("************************************************")
        print("Checkpoint 3")
        print("************************************************")
        return html_code
    except Exception as exception:
        print("************************************************")
        print(exception)
        print("************************************************")
        return flask.redirect('/error')

@app.route('/tutor_avail', methods=['GET'])
def tutor_avail():
    try:
        if sm.checktutor():
            return flask.redirect('/signin')
        # username= auth.authenticate()
        username = flask.session['email']
        # assert(username in tutor_emails)
        print('unms',username)
        id_input = retrievalfunctions.tutor_id_from_email(username)
        print(',ddd',id_input)
        courses = retrievalfunctions.view_tutors_availability_one(id_input)
        # print(courses)
        html_code = flask.render_template('tutor_avail.html',options = courses)
        return html_code
    except Exception:
        return flask.redirect('/error')


@app.route('/studentjoin', methods=['POST'])
def student_join():
    try:
        if sm.checkstudent():
            return flask.redirect('/signin')
        params = flask.request.form
        student_id = retrievalfunctions.student_id_from_email(flask.session['email'])
        # print(student_id,'sid')
        # print(params,'sdfsd11')
        course_id,time_slot,tutor_id = params.get('course_id'),params.get('time_slot'),params.get('tutor_id')
        if retrievalfunctions.check_dup(student_id,course_id,tutor_id,time_slot):
            flask.flash('Your are already enrolled in this course', 'success')
            #courses = retrievalfunctions.view_all_tutors()
            #days = [nearest_day(x[2].replace(' ','_').split('_')[0]) for x in courses]
        # print(list(courses[0]) + [days[0]])
        # fo
            # cs = [tuple(list(course) + [day]) for course,day in zip(courses,days)]
            # html_code = flask.render_template('request_tutor.html',courses= cs)
            return flask.redirect('/requesttutor')

    #     if not retrievalfunctions.write_student_reqs(student_id_input=student_id,course_id_input=course_id,time_slot_input=time_slot,tutor_id_input=tutor_id):
    #         flask.flash('Your have already requested this tutor', 'success')
        print(student_id,course_id,time_slot,tutor_id,'si,ci,ts')
        check_duplicate = retrievalfunctions.check_student_duplicate_enrollment_request(student_id, course_id, time_slot, tutor_id)
        print("********************************************************")
        print("Check_duplicate")
        print(check_duplicate)
        print("********************************************************")
        if check_duplicate == True:
            print("********************************************************")
            print("Checkpoint 1")
            print("********************************************************")
            #html_code = flask.render_template('student_request_failure.html')
            flask.flash(' You have already requested to join this class before.','error')
            print("********************************************************")
            print("Checkpoint 2")
            print("********************************************************")
            return flask.redirect('/requesttutor')
        retrievalfunctions.write_student_reqs(student_id_input=student_id,course_id_input=course_id,time_slot_input=time_slot,tutor_id_input=tutor_id)
        print("********************************************************")
        print("Checkpoint 3")
        print("********************************************************")
        # courses = retrievalfunctions.view_all_tutors()
        # days = [nearest_day(x[2].replace(' ','_').split('_')[0]) for x in courses]
        # print(list(courses[0]) + [days[0]])
        # fo
        # cs = [tuple(list(course) + [day]) for course,day in zip(courses,days)]
        # html_code = flask.render_template('request_tutor.html',courses= cs)
        subject = 'You have received a tutoring request!'
        body = '''You have received a request for an appointment at '''+time_slot.replace('_',' ') +'''

        Login to your portal to view the request

        You can contact the student here: '''+flask.session['email']
        tutor_email = retrievalfunctions.tutor_email_from_id(tutor_id)
        email.send(subject=subject, body=body, email=tutor_email)
        flask.flash('Your request is successful and is under tutor review')
        return flask.redirect('/requesttutor')
        # return flask.redirect('/requesttutor')
    except Exception as exception:
        print("********************************************************")
        print(exception)
        print("********************************************************")
        return flask.redirect('/error')

@app.route('/tutor_add_session', methods=['GET'])
def tutor_add_session():
    try:
        if sm.checktutor():
            return flask.redirect('/signin')
        # courses = retrievalfunctions.view_all_courses()
        # print("**********************************************************")
        # for course in courses:
        #     print(course[0])
        # print("**********************************************************")
        days = ["Monday", "Tuesday", "Wednesday","Thursday", "Friday",
                "Saturday", "Sunday"]
        print(days,'g56')
        st = ['7:00_AM', '7:30_AM', '8:00_AM', '8:30_AM', '9:00_AM', '9:30_AM', '10:00_AM', '10:30_AM', '11:00_AM', '11:30_AM', '12:00_PM', '12:30_PM', '1:00_PM', '1:30_PM', '2:00_PM', '2:30_PM', '3:00_PM', '3:30_PM', '4:00_PM', '4:30_PM', '5:00_PM', '5:30_PM', '6:00_PM', '6:30_PM', '7:00_PM', '07:30_PM', '8:00_PM', '8:30_PM', '9:00_PM', '9:30_PM', '10:00_PM']
        cs = [x[0] for x in retrievalfunctions.view_all_courses()]
        print(cs,'css')
        html_code = flask.render_template('tutor_add_session.html', days = days,st = st,et = st,course_name = cs)
        return html_code
    except Exception:
        return flask.redirect('/error')


def check_time(st,et,day,tutor_id):
    try:
        time_dict = {
            '12:00AM': 0,
            '12:30AM': 0.5,
            '1:00AM': 1,
            '1:30AM': 1.5,
            '2:00AM': 2,
            '2:30AM': 2.5,
            '3:00AM': 3,
            '3:30AM': 3.5,
            '4:00AM': 4,
            '4:30AM': 4.5,
            '5:00AM': 5,
            '5:30AM': 5.5,
            '6:00AM': 6,
            '6:30AM': 6.5,
            '7:00AM': 7,
            '7:30AM': 7.5,
            '8:00AM': 8,
            '8:30AM': 8.5,
            '9:00AM': 9,
            '9:30AM': 9.5,
            '10:00AM': 10,
            '10:30AM': 10.5,
            '11:00AM': 11,
            '11:30AM': 11.5,
            '12:00PM': 12,
            '12:30PM': 12.5,
            '1:00PM': 13,
            '1:30PM': 13.5,
            '2:00PM': 14,
            '2:30PM': 14.5,
            '3:00PM': 15,
            '3:30PM': 15.5,
            '4:00PM': 16,
            '4:30PM': 16.5,
            '5:00PM': 17,
            '5:30PM': 17.5,
            '6:00PM': 18,
            '6:30PM': 18.5,
            '7:00PM': 19,
            '7:30PM': 19.5,
            '8:00PM': 20,
            '8:30PM': 20.5,
            '9:00PM': 21,
            '9:30PM': 21.5,
            '10:00PM': 22,
            '10:30PM': 22.5,
            '11:00PM': 23,
            '11:30PM': 23.5
        }

        start = time_dict[st.replace('_','')]
        end = time_dict[et.replace('_','')]
        dias = retrievalfunctions.tutor_avail_check(day,tutor_id)
        try:
            dias = retrievalfunctions.tutor_avail_check(day,tutor_id)
            ranges = [x[0].split(day)[1][1:].split('-') for x in dias]
            vs = []
            for val in ranges:
                vt = []
                for v in val:
                    vt.append(time_dict[v.replace('_','')])
                vs.append(vt)
            print(vs,'vvs')

            for pos in vs:
                if start == pos[0]:
                    return 'tc'
                elif start > pos[0] and start < pos[1]:
                    return 'tc'
                elif end > pos[0] and end < pos[1]:
                    return 'tc'
                elif end == pos[1]:
                    return 'tc'
                elif start < pos[0] and end > pos[1]:
                    return 'tc'

            # print(ranges,'ranges')
            # for range1 in ranges:
            #     range1 = [time_dict[y] for y in range1]
            #     print(range1)
            # print(ranges,'ranges')
        except Exception as ex:
            print(ex,'eeeee')
            pass
        print(dias,'dias')
        if start >= end:
            return False
        return True
    except Exception:
        return flask.redirect('/error')
@app.route('/send_proposed_session', methods=['POST'])
def send_proposed_session():
    try:
        print(flask.request.form,'formm')
        if sm.checktutor():
            return flask.redirect('/signin')
        print("***************************************************")

        tutor_email = flask.session['email']
        tutor_id = retrievalfunctions.tutor_id_from_email(tutor_email)
        day = flask.request.form.get('day')
        st = flask.request.form.get('st')
        et = flask.request.form.get('et')
        course_name = flask.request.form.get('course')
        # print(course_name,'cnn')
        ot = flask.request.form.get('other_choice')
        # other_choice
        print(day,st,et,course_name,'params')

        # print('ottt',len(ot.replace(' ','')))
        check= False

        if course_name != 'other' and len(ot) > 0:
            contenido = 'Your request could not be submitted. You may either choose an option from the dropdown menu or enter a new course, but doing both is prohibited.'
            flask.flash(contenido,'error')
            return flask.redirect('/tutor_add_session')

        if day is None:
            contenido = "There is no day included in this request"
            flask.flash(contenido,'error')
            return flask.redirect('/tutor_add_session')

        if course_name == 'other' and len(ot.replace(' ','')) == 0:
            contenido = 'Your request could not be submitted. Please make sure to fill in all fields and enter a valid course name (Ex: AP_CALC_BC).'
            contenido += "Make sure that you are not proposing a time when you already have a shift. Contact the admins if you need help."
            flask.flash(contenido,'error')
            return flask.redirect('/tutor_add_session')
            # html_code = flask.render_template('request_failure.html')
            # return html_code

        # time_slot = flask.request.form.get('time_slot')
        # time_slot = day + '_' + st + '_' + et

        if st is None or et is None:
            contenido = 'Your request could not be submitted. Please make sure to fill in all fields and enter a valid course name (Ex: AP_CALC_BC).'
            #contenido += "Make sure that you are not proposing a time when you already have a shift. Contact the admins if you need help."
            flask.flash(contenido,'error')
            return flask.redirect('/tutor_add_session')
            # html_code = flask.render_template('request_failure.html')
            # return html_code

        if not check_time(st,et,day,tutor_id):
            flask.flash('Request could not be completed! Please ensure that the time ranges you have included are valid','error')
            return flask.redirect('/tutor_add_session')
        if check_time(st,et,day,tutor_id) == 'tc':
            flask.flash(f'This conflicts with an existing time on {day}','error')
            return flask.redirect('/tutor_add_session')


        print("*************************************************")
        print("time slot")
        time_slot = day + '_' + st + '-' + et
        print(time_slot)
        print('tss',time_slot)
        print("*************************************************")
        # course_name = flask.request.form.get('course_name')
        # course_name += '\n'
        print
        if course_name is None or course_name == '':
            contenido = 'Your request could not be submitted. Please make sure to fill in all fields and enter a valid course name (Ex: AP_CALC_BC).'
            contenido += "Make sure that you are not proposing a time when you already have a shift. Contact the admins if you need help."
            flask.flash(contenido,'error')
            return flask.redirect('/tutor_add_session')
            # html_code = flask.render_template('request_failure.html')
            # return html_code

        if course_name == 'other':
            new_name = ot.replace(' ','_').upper() + '\n'
            cids = [x[0] for x in retrievalfunctions.course_ids()]
            new_id = random.sample(list(set (range (0,10000) ).symmetric_difference(set(cids))),1)[0]
            retrievalfunctions.new_course(new_name,new_id)
            print('added_course',retrievalfunctions.view_all_courses())
            check = True
            course_name = new_name
        print("*************************************************")
        print("course name")
        print(course_name)
        # print('bool',course_name.replace('\r','') == "AP_WORLD_HISTORY\n")
        # try:
        #     engine = sqlalchemy.create_engine(DATABASE_URL, echo = True)
        #     with engine.connect() as connection:
        #         course_offerings = sqlalchemy.Table('course_offerings',
        #             sqlalchemy.MetaData(), autoload_with = engine)
        #         stmt_select = select(course_offerings.c.course_id).where(course_offerings.c.course_name == f"AP_WORLD_HISTORY\n")
        #         result = connection.execute(stmt_select).fetchall()
        #         print('cres = ',result)
        # except Exception as ex:
        #     print(ex,'cres = ex')
        #     pass
        print("*************************************************")
        # print(course_name in retrievalfunctions.view_all_courses(),'sdfsdfs')
        print(check,'check')
        if not check:
            course_id = retrievalfunctions.course_id_from_course_name(course_name.replace('\r',''))
        else:
            course_id = new_id
        print("*************************************************")
        print("course id = ")
        print(course_id)
        print("***************************************************")
        if course_id == "Can't find course":
            contenido = 'Your request could not be submitted. Please make sure to fill in all fields and enter a valid course name (Ex: AP_CALC_BC).'
            contenido += "Make sure that you are not proposing a time when you already have a shift. Contact the admins if you need help."
            flask.flash(contenido,'error')
            return flask.redirect('/tutor_add_session')
            # html_code = flask.render_template('request_failure.html')
            # return html_code
        check_duplication = retrievalfunctions.check_tutor_availability(tutor_id, time_slot)
        print("*************************************************")
        print("Check duplication")
        print(check_duplication)
        print("**************************************************")
        if check_duplication is True:
            contenido = 'Your request could not be submitted. Please make sure to fill in all fields and enter a valid course name (Ex: AP_CALC_BC).'
            contenido += "Make sure that you are not proposing a time when you already have a shift. Contact the admins if you need help."
            flask.flash(contenido,'error')
            return flask.redirect('/tutor_add_session')
            # html_code = flask.render_template('request_failure.html')
            # return html_code
        if retrievalfunctions.check_tutor_duplicate_teach_request(time_slot_input=time_slot,
                    course_id_input=course_id,tutor_id_input=tutor_id) is True:
            flask.flash('You have already submitted a request with this information')
            return flask.redirect('/tutor_add_session')
        add_request = retrievalfunctions.add_tutor_reqs(tutor_id, time_slot, course_id)
        if add_request == True:
            # html_code = flask.render_template('request_success.html')
            # return html_code
            flask.flash('Your request has been submitted','success')
            return flask.redirect('/tutor_add_session')
        else:
            contenido = 'Your request could not be submitted. Please make sure to fill in all fields and enter a valid course name (Ex: AP_CALC_BC).'
            contenido += "Make sure that you are not proposing a time when you already have a shift. Contact the admins if you need help."
            flask.flash(contenido,'error')
            return flask.redirect('/tutor_add_session')
            # html_code = flask.render_template('request_failure.html')
            # return html_code
    except Exception:
        return flask.redirect('/error')

@app.route('/tutor_remove_session', methods=['GET'])
def tutor_remove_session():
    try:
        if sm.checktutor():
            return flask.redirect('/signin')
        tutor_email = flask.session['email']
        tutor_id = retrievalfunctions.tutor_id_from_email(tutor_email)
        tutor_calendar = retrievalfunctions.view_my_availability(tutor_id)
        # print("**********************************************************")
        # for session in tutor_calendar:
        #     print(session[0])
        # print("**********************************************************")
        html_code = flask.render_template('tutor_remove_session.html', options = tutor_calendar)
        return html_code
    except Exception:
        return flask.redirect('/error')

@app.route('/request_to_remove', methods=['POST'])
def request_to_remove():
    try:
        if sm.checktutor():
            return flask.redirect('/signin')
        tutor_email = flask.session['email']
        print("**********************************************************")
        print("tutor email")
        print(tutor_email)
        print("**********************************************************")
        tutor_id = retrievalfunctions.tutor_id_from_email(tutor_email)
        print("**********************************************************")
        print("tutor_id")
        print(tutor_id)
        print("**********************************************************")
        time_slot = flask.request.form['time_slot']
        print("**********************************************************")
        print("time slot")
        print(time_slot)
        print("**********************************************************")
        course_name = flask.request.form['course_name'].replace('\r','')
        print("**********************************************************")
        print("course_name")
        print(course_name)
        print(course_name == "ANATOMY\n")
        print(course_name.replace('\n','_'))
        print("**********************************************************")
        course_id = retrievalfunctions.course_id_from_course_name(course_name)
        print("**********************************************************")
        print("course_id")
        print(course_id)
        print("**********************************************************")
        check_duplicate = retrievalfunctions.check_tutor_duplicate_remove_request(tutor_id, time_slot, course_id)
        print("**********************************************************")
        print("check_duplicate")
        print(check_duplicate)
        print("**********************************************************")
        if check_duplicate == True:
            print("**********************************************************")
            print("Checkmark 1")
            print("**********************************************************")
            # html_code = flask.render_template('tutor_remove_request_failure.html')
            # print("**********************************************************")
            # print("Checkmark 2")
            # print("**********************************************************")
            # return html_code
            flask.flash('Your request could not be submitted. You have already requested to remove this course before.')
            return flask.redirect('/tutor_remove_session')
        print("**********************************************************")
        print("Checkmark 3")
        print("**********************************************************")
        add_request = retrievalfunctions.add_tutor_remove_request(tutor_id, time_slot, course_id)
        print("**********************************************************")
        print("add_request")
        print(add_request)
        print("**********************************************************")
        if add_request == True:
            # html_code = flask.render_template('request_success.html')
            # return html_code
            flask.flash('Remove Request successful','success')
        else:
            # html_code = flask.render_template('remove_request_failure.html')
            # return html_code
            flask.flash('Remove Request Failed','error')
        return flask.redirect('/tutor_remove_session')
    except Exception:
        return flask.redirect('/error')

