from django.urls import re_path
from .consumer import GameConsumer

websocket_urlpatterns = [
	re_path(r'ws/play/(?P<gameID>\d+)/(?P<token>\w+)/', GameConsumer.as_asgi()),
]