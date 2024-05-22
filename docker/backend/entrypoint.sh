#!/bin/sh
set -e

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

gunicorn config.asgi:application -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000