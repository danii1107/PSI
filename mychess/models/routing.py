from django.urls import path
from .consumers import ChessConsumer

websocket_urlpatterns = [
    path("ws/play/<int:gameID>/", ChessConsumer.as_asgi()),
]
