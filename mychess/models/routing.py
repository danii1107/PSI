"""
Modulo que se encarga de enrutar las peticiones de websocket
a los consumidores correspondientes.
@Author: Daniel Birsan
"""

from django.urls import re_path
from .consumers import ChessConsumer

# Expresion regular que captura cualquier entero con el formato
websocket_urlpatterns = [
    re_path(r'ws/play/(?P<gameID>\d+)/', ChessConsumer.as_asgi()),
]
