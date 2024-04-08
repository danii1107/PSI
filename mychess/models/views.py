"""
Modulo para la vista de los WebSockets.
@autor: Daniel Birsan
"""

from django.shortcuts import render
from django.views.generic import View


class ChessTemplateView(View):
    """
        Clase que se encarga de renderizar la plantilla
        de la aplicacion.
        @autor: Daniel Birsan
        @metodos: get
    """
    def get(self, request, *args, **kwargs):
        """
            Metodo que renderiza la plantilla de la aplicacion
            y le pasa los parametros necesarios al script.
            @autor: Daniel Birsan
            @param: request, *args, **kwargs
        """
        # Obtiene el gameID de la url
        gameID = kwargs.get('gameID')

        # Obtiene el token_key de los parametros de la petición
        query_string = request.META.get('QUERY_STRING', '')
        token_key = query_string.split('&')[0] if query_string else ''

        context = {
            'gameID': gameID,
            'token_key': token_key
        }
        # Renderiza la plantilla
        return render(request, 'mychess_template.html', context)
