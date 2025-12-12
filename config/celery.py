import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')

from celery import Celery


app = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
