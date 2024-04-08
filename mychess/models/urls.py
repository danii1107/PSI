"""
Modulo que contiene las rutas de la aplicacion.
@autor: Enrique Gómez Fernández
"""

from django.urls import path
from models.api import MyTokenCreateView, ChessGameViewSet

urlpatterns = [
    path('mytokenlogin/', MyTokenCreateView.as_view()),
    path('games/',
         ChessGameViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='games'),
    path('games/<int:pk>/',
         ChessGameViewSet.as_view({'get': 'retrieve'}),
         name='games-detail'),
]
