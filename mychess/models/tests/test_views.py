from django.test import TestCase
from django.urls import reverse
from django.http import HttpRequest
from django.template.loader import render_to_string
from .views import ChessTemplateView

class ChessTemplateViewTest(TestCase):
    def test_get(self):
        view = ChessTemplateView()
        request = HttpRequest()
        request.method = 'GET'
        response = view.get(request, gameID=123, token='abc123')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mychess_template.html')

        expected_html = render_to_string('mychess_template.html', {'gameID': 123, 'token': 'abc123'})
        self.assertContains(response, expected_html)
