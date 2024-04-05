from django.shortcuts import render
from django.views.generic import View

class ChessTemplateView(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'mychess_template.html')