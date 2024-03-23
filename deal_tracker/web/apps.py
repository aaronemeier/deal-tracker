from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class WebConfig(AppConfig):
    name = "deal_tracker.web"
    label = "web"
    verbose_name = _("Web")

    def ready(self) -> None:
        from django.conf import settings  # pylint: disable=import-outside-toplevel
        from os import getenv  # pylint: disable=import-outside-toplevel

        print(
            f"Using settings: DJANGO_SETTINGS_MODULE={getenv('DJANGO_SETTINGS_MODULE')} DEBUG={settings.DEBUG}, "
            f"DB_HOST={settings.DATABASES['default']['HOST']}, "
            f"DB_NAME={settings.DATABASES['default']['NAME']}"
        )
