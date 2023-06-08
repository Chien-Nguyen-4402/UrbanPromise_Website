#----------------------------------------------------------------------
# Author: Lois I Omotara
# securitymeasures.py
#----------------------------------------------------------------------
import retrievalfunctions as rf
import auth
import flask

def checkadmin():
    email = auth.authenticate()
    if rf.check_admininfo_dup(email):
        return False
    else:
        flask.flash('You are not authorized to access this page')
        return True

def checktutor():
    email = auth.authenticate()
    if rf.check_tutorinfo_dup(email):
        return False
    else:
        flask.flash('You are not authorized to access this page')
        return True

def checkstudent():
    email = auth.authenticate()
    if rf.check_studentinfo_dup(email):
        return False
    else:
        flask.flash('You are not authorized to access this page')
        return True
