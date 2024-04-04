from django.urls import path
from models.mychess import myclassView
from models.api import MyTokenCreateView, ChessGameViewSet

urlpatterns = [
    path(r'myclassView/', myclassView.as_view()),
    path(r'api/v1/mytokenlogin/', MyTokenCreateView.as_view()),
    path(r'api/v1/games/', ChessGameViewSet.as_view, name='games'),
]