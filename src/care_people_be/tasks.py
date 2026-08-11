from celery import current_app, shared_task
from celery.schedules import crontab
from django.utils.timezone import now


@shared_task
def periodic_task_example():
    pass


@current_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    pass
