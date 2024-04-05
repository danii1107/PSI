from django.shortcuts import render
from django.views.generic import View

class ChessTemplateView(View):
	def get(self, request, *args, **kwargs):
		context = {
			'gameID': kwargs.get('gameID'),
			'token': kwargs.get('token')
		}
		return render(request, 'mychess_template.html', context)