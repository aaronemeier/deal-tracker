# Deal Tracker
**Discontinued**

Simple Web App to track prices of Swiss online shops and notify users when the price drops below a certain threshold.

## Run Development

```bash
cp .env.example .env
docker-compose up -d
```

Apply migrations and create a superuser:

```bash
docker-compose run web /bin/bash
```

```bash
python manage.py migrate
export DJANGO_SUPERUSER_USERNAME=admin
export DJANGO_SUPERUSER_EMAIL=admin@example.com
export DJANGO_SUPERUSER_PASSWORD=password
export DJANGO_SUPERUSER_FIRST_NAME=System
export DJANGO_SUPERUSER_LAST_NAME=Administrator
python manage.py createsuperuser --noinput
```
