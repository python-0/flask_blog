from flask.ext.mail import Message
from flask import current_app, render_template
from threading import Thread
from . import mail


def send_mail(to,subject,template,**kwargs):
    app = current_app._get_current_object()
    msg = Message(current_app.config['FLASKY_MAIL_PREFIX'] + subject,
                  sender=app.config['MAIL_USERNAME'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs )
    msg.html = render_template(template + '.html', **kwargs )
    thr = Thread(target=send_async_email,args=[app, msg])
    thr.start()
    return thr


def send_async_email(app,msg):
    with app.app_context():
        mail.send(msg)
