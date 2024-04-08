#!/bin/bash
export DJANGO_SUPERUSER_EMAIL='alumnodb@alumnodb.com'
export DJANGO_SUPERUSER_USERNAME='alumnodb'
export DJANGO_SUPERUSER_PASSWORD='alumnodb'
python3.11 manage.py createsuperuser --noinput
daphne -b 0.0.0.0 mychess.asgi:application
