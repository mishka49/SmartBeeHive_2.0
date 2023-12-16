import time

from Diplom.celery import app

from .services import *


@app.task
def beat_clear_outdated_data_from_model():
    # time.sleep(0)
    print('Task is completed')
    return 'All is good'


