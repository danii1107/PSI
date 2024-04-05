from django.urls import path
from models.mychess import myclassView
from models.api import MyTokenCreateView, ChessGameViewSet

urlpatterns = [
    path(r'myclassView/', myclassView.as_view()),
    path( 'mytokenlogin/', MyTokenCreateView.as_view()),
    path('games/', ChessGameViewSet.as_view({'get': 'list', 'post': 'create'}), name='games'),
    path('games/<int:pk>/', ChessGameViewSet.as_view({'get': 'retrieve'}), name='games-detail'),
]