from django.shortcuts import render
from django.views.generic import View

class ChessTemplateView(View):
	def get(self, request, *args, **kwargs):
		gameID = kwargs.get('gameID')
		token_key = request.GET.get('token_key')

		context = {
			'gameID': gameID,
			'token_key': token_key
		}
		return render(request, 'mychess_template.html', context)