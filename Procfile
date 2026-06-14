release: python manage.py migrate && python manage.py collectstatic --noinput
web: gunicorn cuerposano.wsgi:application
worker: python manage.py qcluster
