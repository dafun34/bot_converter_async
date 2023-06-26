import asyncio

import pytz
from celery import Celery
from celery.schedules import crontab

from commands.update_currencies import get_currencies_for_db
from tasks import send_currencies_summary

app = Celery(
    "tasks", broker="redis://redis:6379", backend="redis://redis:6379"
)

app.conf.timezone = pytz.timezone("Europe/Moscow")


@app.task
def my_periodic_task():
    print("This is a periodic task")


@app.task
def send_currencies_summary_task():
    asyncio.get_event_loop().run_until_complete(send_currencies_summary())


@app.task
def update_currencies_task():
    asyncio.get_event_loop().run_until_complete(get_currencies_for_db())


app.conf.beat_schedule = {
    "send_currencies_summary_task": {
        "task": "celery_app.send_currencies_summary_task",
        "schedule": crontab(hour=9, minute=0),
    },
    "update_currencies_task": {
        "task": "celery_app.update_currencies_task",
        "schedule": crontab(hour=11, minute=10),
    },
}
