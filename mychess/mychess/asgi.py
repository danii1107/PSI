"""
Modulo que contiene la configuración de los protocolos
para los WebSockets.
@autor: Daniel Birsan
"""

import os

# Obtiene la configuración de los WebSockets
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mychess.settings')

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application

# Obtiene la aplicación ASGI de Django
django_asgi_app = get_asgi_application()

import models.routing

# Configura los protocolos de la aplicación
application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': AuthMiddlewareStack(
        URLRouter(models.routing.websocket_urlpatterns)
    ),
})
