from datetime import datetime

from django.core.mail import send_mail

from dmess.celery import app


@app.task
def sendmail():
    send_mail(
        'Subject here',
        'Here is the message. Send datetime: {}'.format(datetime.now()),
        'noreply@asmirnov.me',
        ['noreply@asmirnov.me'],
        fail_silently=False,
    )
