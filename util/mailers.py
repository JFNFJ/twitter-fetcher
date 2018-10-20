import os
from flask_mail import Mail, Message
from settings import app


class ResetPasswordMailer:

    @classmethod
    def send_email(cls, email, subject, html):
        mail = Mail(app)
        with app.app_context():
            msg = Message(subject=subject,
                          sender=os.getenv("MAIL_USERNAME"),
                          recipients=[email],
                          html=html)
            mail.send(msg)
