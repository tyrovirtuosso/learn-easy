import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'learn_easy.settings')

app = Celery('learn_easy')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()