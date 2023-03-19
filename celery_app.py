import asyncio
from celery import Celery
from tasks import send_test_messages

app = Celery("tasks", broker='redis://redis:6379', backend='redis://redis:6379')


@app.task
def my_periodic_task():
    print('This is a periodic task')


@app.task
def test_task():
    asyncio.get_event_loop().run_until_complete(send_test_messages())


app.conf.beat_schedule = {
    'test_task': {
        'task': "celery_app.test_task",
        'schedule': 10,
    },
}

