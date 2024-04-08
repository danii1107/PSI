from django.shortcuts import render
from django.views.generic import View


class ChessTemplateView(View):
    def get(self, request, *args, **kwargs):
        gameID = kwargs.get('gameID')

        query_string = request.META.get('QUERY_STRING', '')
        token_key = query_string.split('&')[0] if query_string else ''

        context = {
            'gameID': gameID,
            'token_key': token_key
        }
        return render(request, 'mychess_template.html', context)
