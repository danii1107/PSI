from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse
from rest_framework.test import APIClient
from models.models import ChessGame
from rest_framework.authtoken.models import Token


class ChessGameViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='12345'
        )
        self.game = ChessGame.objects.create(
            status=ChessGame.ACTIVE,
            board_state='initial_state',
            start_time=timezone.now(),
            timeControl='10+0',
            blackPlayer=self.user,
            whitePlayer=self.user
        )
        self.token = Token.objects.create(user=self.user)

    def test_list(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('mychess_template', kwargs={'gameID': self.game.id})
        url = url + '?' + self.token.key
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
