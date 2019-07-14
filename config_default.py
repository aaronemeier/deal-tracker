
DATABASE ={

}

LANGUAGE_CODE = "de-CH"
TIME_ZONE = "Europe/Zurich"
PRODUCTION = False
SECRET_KEY = "(yhmd&v@l&syc56*8^%(h17ucs%&7unwx6(d!=$#&jyss^##%o"
ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../../dealtracker/db.sqlite3'),
    }
}
# TODO: Change this for heroku prod
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'USER': "username",
        'PASSWORD': 'password',
        'HOST': '127.0.0.1',
        'PORT': '5432'
    }
}
"""


SENDGRID_API_KEY = ""
EMAIL_HOST = "smtp.sendgrid.net"
EMAIL_HOST_USER = "pikey"
EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
EMAIL_PORT = 587
EMAIL_USE_TLS = True
