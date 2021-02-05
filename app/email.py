from app import mail, app
from flask_mail import Message
from flask import render_template
from threading import Thread

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_mail(sender, recipients, subject, body, html):
    msg = Message(subject, sender=sender, recipients=recipients )
    msg.body = body 
    msg.html = html 
    Thread(target = send_async_email, args = (app, msg)).start()


def send_password_reset_mail(user):
    token = user.generate_reset_password_token()
    send_mail( app.config['MAIL_USERNAME'], 
              [user.email], 
              '[Journyy] Password Reset link.',
              render_template('email/reset.txt', user=user, token=token),
              render_template('email/reset.html', user=user, token=token)
            )


