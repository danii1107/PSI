from django.urls import path
from models.mychess import myclassView

urlpatterns = [
    path(r'myclassView/', myclassView.as_view()),
]