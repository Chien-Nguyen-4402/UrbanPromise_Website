#----------------------------------------------------------------------
# Author: Lois
# email_notifs.py
#----------------------------------------------------------------------
import smtplib, ssl
import smtplib, ssl
from email.mime.text import MIMEText

def send(body, subject,email):
    port = 465  # For SSL
    password = "jnhm cvuh rflz ssbc"
    sender_email ="urbanpromise0@gmail.com"
    receiver_email = email
    message = MIMEText(body)
    message['Subject'] = subject
    message['From'] = sender_email
    message['To'] = receiver_email

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, [receiver_email], message.as_string())
        print('sent')


