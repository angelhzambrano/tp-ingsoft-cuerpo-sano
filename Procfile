release: python manage.py migrate && python manage.py create_default_user && python manage.py collectstatic --noinput
web: gunicorn cuerposano.wsgi:application
