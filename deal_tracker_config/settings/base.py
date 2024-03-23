from datetime import timedelta
from logging import getLevelName
from pathlib import Path

import environ
from django.utils.translation import gettext_lazy as _

import deal_tracker_config.build_config

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
APPS_DIR = ROOT_DIR / "deal_tracker"
ENV_FILE = ROOT_DIR / ".env"

env = environ.Env()

if ENV_FILE.exists():
    print(f"Loading .env configuration from: {ENV_FILE}")
    env.read_env(str(ROOT_DIR / ".env"))

# SITE
# -----------------------------------------------------------------------------
SITE_VERSION = deal_tracker_config.build_config.SITE_VERSION
SITE_INSTANCE_NAME = env.str("SITE_INSTANCE_NAME", default="deal_tracker_local")

# GENERAL
# -----------------------------------------------------------------------------
DEBUG = env.bool("DJANGO_DEBUG", False)
TIME_ZONE = "UTC"
LANGUAGE_CODE = "en"
LANGUAGES = [
    ("en", _("English")),
    ("de", _("German")),
]
USE_I18N = True
USE_TZ = True
LOCALE_PATHS = [str(ROOT_DIR / "locale")]
SECRET_KEY = env.str("DJANGO_SECRET_KEY", default="secret")
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["*"])
CSRF_TRUSTED_ORIGINS = env.list("DJANGO_CSRF_TRUSTED_ORIGINS", default=["http://localhost:8000"])

# DATABASES
# -----------------------------------------------------------------------------
# Using BigAutoField for default PKs, because this will be the default in the future
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
DATABASES = {"default": env.db("DATABASE_URL", default="postgres://postgres:postgres@localhost/postgres")}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

# URLS
# -----------------------------------------------------------------------------
ROOT_URLCONF = "deal_tracker_config.urls"
WSGI_APPLICATION = "deal_tracker_config.wsgi.application"
ASGI_APPLICATION = "deal_tracker_config.asgi.application"

# APPS
# -----------------------------------------------------------------------------
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
THIRD_PARTY_APPS = [
    "crispy_forms",
    "crispy_bootstrap4",
    "django_registration",
    "axes",
    "django_celery_results",
    "django_celery_beat",
    "captcha",
    "health_check",
    "health_check.db",
    "health_check.cache",
    "health_check.storage",
]
LOCAL_APPS = [
    "deal_tracker.web.apps.WebConfig",
]
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# AUTHENTICATION
# -----------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = ["axes.backends.AxesBackend", "django.contrib.auth.backends.ModelBackend"]

# PASSWORDS
# -----------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# MIDDLEWARE
# -----------------------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "deal_tracker.web.middleware.ThemeMiddleware",
    "deal_tracker.web.middleware.UserLanguageMiddleware",
    "axes.middleware.AxesMiddleware",
]

# STATIC
# -----------------------------------------------------------------------------
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}
STATIC_HOST = env.str("DJANGO_STATIC_HOST", "")  # CDN Host
STATIC_ROOT = str(ROOT_DIR / "staticfiles")
STATIC_URL = f"{STATIC_HOST}/assets/static/"
STATICFILES_DIRS = [str(APPS_DIR / "static")]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# MEDIA
# -----------------------------------------------------------------------------
MEDIA_ROOT = str(ROOT_DIR / "mediafiles")
MEDIA_URL = "/assets/media/"

# TEMPLATES
# -----------------------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(APPS_DIR / "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# EMAIL
# -----------------------------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_TIMEOUT = 5
DEFAULT_FROM_EMAIL = env.str("DEFAULT_FROM_EMAIL", "root@localhost")
EMAIL_CONFIG = env.email("DJANGO_EMAIL_URL", default="smtp://username:password@localhost/")
EMAIL_HOST = EMAIL_CONFIG["EMAIL_HOST"]
EMAIL_HOST_USER = EMAIL_CONFIG["EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD = EMAIL_CONFIG["EMAIL_HOST_PASSWORD"]
EMAIL_PORT = EMAIL_CONFIG["EMAIL_PORT"]
EMAIL_USE_TLS = EMAIL_CONFIG.get("EMAIL_USE_TLS", False)

# ADMIN
# -----------------------------------------------------------------------------
ADMIN_URL = env.str("DJANGO_ADMIN_URL", "admin") + "/"
ADMINS = [("""Aaron Meier""", "aaron@0x41.ch")]
MANAGERS = ADMINS

# LOGGING
# -----------------------------------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        }
    },
    "handlers": {
        "console": {"level": "DEBUG", "class": "logging.StreamHandler", "formatter": "verbose"},
    },
    "root": {"level": "INFO", "handlers": ["console"], "propagate": False},
    "loggers": {
        "django": {
            "level": "INFO" if DEBUG else "WARN",
            "handlers": ["console"],
            "propagate": False,
        },
        "deal_tracker": {
            "handlers": ["console"],
            "level": env.str("DJANGO_LOG_LEVEL", default="INFO"),
            "propagate": False,
        },
        "celery": {
            "handlers": ["console"],
            "level": env.str("DJANGO_LOG_LEVEL", default="INFO"),
            "propagate": False,
        },
        "django.db.backends": {
            "handlers": ["console"],
            "level": env.str("DJANGO_LOG_LEVEL_DATABASE", default="WARNING"),
            "propagate": False,
        },
    },
}

# CELERY
# -----------------------------------------------------------------------------
CELERY_TIMEZONE = TIME_ZONE
CELERY_BROKER_URL = env.cache("CELERY_BROKER_URL", default="redis://")
CELERY_RESULT_BACKEND = "django-db"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_TIME_LIMIT = 5 * 60
CELERY_TASK_SOFT_TIME_LIMIT = 60
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
CELERY_CACHE_BACKEND = "django-cache"
CELERY_TASK_TRACK_STARTED = True
CELERY_RESULT_EXPIRES = timedelta(days=5) if DEBUG else timedelta(days=30)
CELERY_RESULT_EXTENDED = True
CELERY_TASK_LOCK_CACHE = "default"
CELERY_ENABLE_SCHEDULED_TASKS = env.bool("CELERY_ENABLE_SCHEDULED_TASKS", default=True)
CELERY_BROKER_TRANSPORT_OPTIONS = {"global_keyprefix": f"{SITE_INSTANCE_NAME}:"}

# AXES
# -----------------------------------------------------------------------------
AXES_ENABLED = False
AXES_FAILURE_LIMIT = 10
AXES_COOLOFF_TIME = 10
AXES_ONLY_ADMIN_SITE = True
AXES_LOCKOUT_TEMPLATE = "axes/lockout.html"
AXES_VERBOSE = False
AXES_IPWARE_META_PRECEDENCE_ORDER = [
    "HTTP_X_FORWARDED_FOR",
    "REMOTE_ADDR",
]

# SENTRY
# -----------------------------------------------------------------------------
SENTRY_DSN = env.str("SENTRY_DSN", default=None)
SENTRY_DJANGO_LOG_LEVEL = getLevelName(env.str("SENTRY_DJANGO_LOG_LEVEL", default="INFO"))

if SENTRY_DSN is not None:
    import logging

    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    from sentry_sdk.integrations.logging import LoggingIntegration
    from sentry_sdk.integrations.celery import CeleryIntegration
    from sentry_sdk.integrations.redis import RedisIntegration

    sentry_logging = LoggingIntegration(
        level=SENTRY_DJANGO_LOG_LEVEL,  # Capture info and above as breadcrumbs
        event_level=logging.ERROR,  # Send errors as events
    )
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[
            DjangoIntegration(),
            LoggingIntegration(),
            CeleryIntegration(),
            RedisIntegration(),
        ],
        environment=env.str("SENTRY_ENVIRONMENT", default="production"),
        release=SITE_VERSION,
        # Times an error is sampled and sent to Sentry
        # Set to 1.0 to capture 100% of errors sent
        sample_rate=env.float("SENTRY_SAMPLE_RATE", 0.1),
        # Times a transaction is sampled and sent to Sentry
        # Set to 1.0 to capture 100% of transactions for performance monitoring
        traces_sample_rate=env.float("SENTRY_TRACES_SAMPLE_RATE", default=0.0),
        send_default_pii=True,
    )

# HEALTH
# -----------------------------------------------------------------------------
HEALTH_CHECK = {
    "DISK_USAGE_MAX": 90,
    "MEMORY_MIN": 100,
}
REDIS_URL = CELERY_BROKER_URL

# DJANGO REGISTRATION
# -----------------------------------------------------------------------------
LOGIN_URL = "/login"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
ACCOUNT_ACTIVATION_DAYS = env.int("ACCOUNT_ACTIVATION_DAYS", default=7)
REGISTRATION_OPEN = env.bool("REGISTRATION_OPEN", default=True)

# CRISPY BOOTSTRAP
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = "bootstrap4"

# RECAPTCHA
# -----------------------------------------------------------------------------
RECAPTCHA_PUBLIC_KEY = env.str("RECAPTCHA_PUBLIC_KEY", default="6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI")
RECAPTCHA_PRIVATE_KEY = env.str("RECAPTCHA_PRIVATE_KEY", default="6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe")
SILENCED_SYSTEM_CHECKS = ["captcha.recaptcha_test_key_error"]

# PROXY
# -----------------------------------------------------------------------------
HTTP_PROXY_LIST = env.list("HTTP_PROXY_LIST", default=[])
HTTPS_PROXY_LIST = env.list("HTTPS_PROXY_LIST", default=[])
