from celery import Celery
from celery.schedules import crontab

app = Celery("tasks", broker='redis://redis:6379', backend='redis://redis:6379')

from datetime import timedelta


@app.task
def my_periodic_task():
    print('This is a periodic task')


app.conf.beat_schedule = {
    'my-periodic-task': {
        'task': 'celery_app.my_periodic_task',
        'schedule': timedelta(seconds=10),
    },
}

