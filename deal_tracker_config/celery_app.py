import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "deal_tracker_config.settings.production")

app = Celery("deal_tracker")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
