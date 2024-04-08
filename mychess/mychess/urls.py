"""
Modulo que contiene las rutas del proyecto.
@autor: Enrique Gómez Fernández
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from models.views import ChessTemplateView

# Rutas del proyecto y vistas asociadas
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('djoser.urls')),
    path('api/v1/', include('djoser.urls.authtoken')),
    path('api/v1/', include('models.urls')),
    path('ws/play/<int:gameID>/',
         ChessTemplateView.as_view(),
         name='mychess_template'),
    path('', RedirectView.as_view(url='/api/v1/', permanent=True)),
]
