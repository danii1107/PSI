from django.urls import re_path
from .consumer import GameConsumer

websocket_urlpatterns = [
	re_path(r'ws/mychess/(?P<room_name>\w+)/', GameConsumer.as_asgi()),
]