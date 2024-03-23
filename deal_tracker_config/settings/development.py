import socket
from _socket import gaierror

from .base import *  # noqa

# GENERAL
# -----------------------------------------------------------------------------
DEBUG = True
ALLOWED_HOSTS = ["*"]

# APPS
# -----------------------------------------------------------------------------
INSTALLED_APPS += ["whitenoise.runserver_nostatic", "django_extensions", "debug_toolbar"]
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]  # noqa F405

try:
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]

except gaierror:
    # Catch error on macOS (where $HOSTNAME is not set in /etc/hosts)
    pass

# CACHES
# ------------------------------------------------------------------------------
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

# EMAIL
# -----------------------------------------------------------------------------
EMAIL_HOST = "localhost"
EMAIL_PORT = 1025
