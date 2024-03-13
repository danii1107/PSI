from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import ChessMove, ChessGame
from .consumer_main import _init

class ConsumerMainTestCase(TestCase):
    def setUp(self):
        self.user1, self.user1_token, self.user2, self.game = _init()

    def test_init(self):
        # Check if the database is cleaned
        self.assertEqual(ChessMove.objects.count(), 0)
        self.assertEqual(ChessGame.objects.count(), 0)
        self.assertEqual(User.objects.count(), 0)

        # Check if the users are created
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.first().username, 'user1@example.com')
        self.assertEqual(User.objects.last().username, 'user2@example.com')

        # Check if the tokens are created
        self.assertEqual(Token.objects.count(), 1)
        self.assertEqual(Token.objects.first().user, self.user1)

        # Check if the game is created correctly
        self.assertEqual(ChessGame.objects.count(), 1)
        self.assertEqual(self.game.whitePlayer, self.user1)

    def test_init_with_black_player(self):
        user1, user1_token, user2, game = _init(consumerFirst=False)
        self.assertEqual(game.blackPlayer, user1)