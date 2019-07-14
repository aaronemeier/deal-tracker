import logging
from django.apps import AppConfig


class DealtrackerAppConfig(AppConfig):
    name = "dealtracker_frontend"

    def ready(self):
        logging.basicConfig(level=logging.INFO)
