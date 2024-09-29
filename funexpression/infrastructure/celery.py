from celery import Celery

app = Celery(
        'geo',
        broker='pyamqp://admin:pass@rabbitmq:5672//',
        include=[
            'infrastructure.clients.geo_service'
            # 'tasks.geo_task'
        ]
    )
