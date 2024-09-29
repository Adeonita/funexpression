from celery import Celery

app = Celery(
        'geo',
        broker='pyamqp://admin:pass@rabbitmq:5672//',
        include=[
            'tasks.geo_task'
        ]
    )