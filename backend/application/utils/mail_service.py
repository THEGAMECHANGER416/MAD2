from flask_mail import Mail, Message
from flask import current_app

def send_mail(to, subject, template=None, **kwargs):
    msg = Message(subject, recipients=[to])
    if template is not None:
        msg.body = render_template(template + '.txt', **kwargs)
        msg.html = render_template(template + '.html', **kwargs)
    else:
        msg.body = "Test"

    current_app.extensions['mail'].send(msg)