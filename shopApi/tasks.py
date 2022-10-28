from account.models import SpamContacts
from .celery import app
from account.send_email import send_confirmation_email
from django.core.mail import send_mail


@app.task
def send_email_task(user, code):
    send_confirmation_email(user, code)


@app.task
def send_spam_email():
    for user in SpamContacts.objects.all():
        send_mail(
            'Spam Spam Spam',
            'This spam letter for you by Kurmanjan!',
            'kurmanjan25nurbekova@gmail.com',
            [user.email],
            fail_silently=False,
        )