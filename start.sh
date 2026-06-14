#!/bin/bash
set -e

echo "🔄 Ejecutando migraciones..."
python manage.py migrate

echo "👤 Creando usuario por defecto..."
python manage.py create_default_user || true

echo "📦 Recolectando estáticos..."
python manage.py collectstatic --noinput

echo "🚀 Iniciando gunicorn..."
gunicorn cuerposano.wsgi:application
