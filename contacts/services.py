from django.core.mail import send_mail

from Diplom.settings import EMAIL_HOST_USER
from detector.models import CriticalSituationsModel


def send(user_email, title, message):
    send_mail(
        title,
        message,
        'smartbeehive.messages@gmail.com',
        [user_email],
        fail_silently=False,
    )


