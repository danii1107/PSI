#!/bin/bash
export DJANGO_SUPERUSER_EMAIL='alumnodb@alumnodb.com'
export DJANGO_SUPERUSER_USERNAME='alumnodb'
export DJANGO_SUPERUSER_PASSWORD='alumnodb'
python3.11 manage.py shell -c "from models.models import Player; Player.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').delete()"
if python3.11 manage.py createsuperuser --no-input; then
    echo "Superusuario creado con éxito."
else
    echo "No se pudo crear el superusuario. Es posible que ya exista o haya un problema con las variables de entorno."
fi
daphne -b 0.0.0.0 mychess.asgi:application
