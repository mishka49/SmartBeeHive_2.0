from send_email.celery import app

from authentication.models import User
from .services import send


@app.task
def send_email_swarming(user: User, hive):
    send(user.email,
         f'ВНИМАНИЕ! Роение',
         f'Произошло роение в улье {hive.id}'
         )


