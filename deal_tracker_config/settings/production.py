from .base import *  # noqa

# GENERAL
# ------------------------------------------------------------------------------
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["localhost"])
try:
    from socket import gethostname, gethostbyname, gaierror

    ALLOWED_HOSTS.append(gethostname())  # Allow hostname
    ALLOWED_HOSTS.append(gethostbyname(gethostname()))  # Allow IP
except gaierror:
    # Catch error on macOS (where $HOSTNAME is not set in /etc/hosts)
    pass

# DATABASES
# ------------------------------------------------------------------------------
DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=60)

# EMAIL
# ------------------------------------------------------------------------------
DEFAULT_FROM_EMAIL = env.str("DJANGO_DEFAULT_FROM_EMAIL", default="Deal Tracker <noreply@example.com>")
SERVER_EMAIL = env.str("DJANGO_SERVER_EMAIL", default=DEFAULT_FROM_EMAIL)

# AXES
# -----------------------------------------------------------------------------
AXES_ENABLED = True
