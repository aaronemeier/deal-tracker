# Docs

## Maintenance

### Migrations

```bash
python manage.py showmigrations
python manage.py migrate
python manage.py makemessages -l de
python manage.py compilemessages
```

### Create a superuser

```bash
export DJANGO_SUPERUSER_USERNAME=admin
export DJANGO_SUPERUSER_EMAIL=admin@example.com
export DJANGO_SUPERUSER_PASSWORD=password
export DJANGO_SUPERUSER_FIRST_NAME=System
export DJANGO_SUPERUSER_LAST_NAME=Administrator
python manage.py createsuperuser --noinput
```

### Destroy DB

```bash
docker-compose down && docker volume rm -f deal-tracker-backend_postgres
```
