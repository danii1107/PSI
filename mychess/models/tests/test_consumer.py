from channels.testing import ChannelsLiveServerTestCase
from rest_framework.authtoken.models import Token
from models.consumers import ChessConsumer
from models.models import ChessGame, ChessMove
from django.contrib.auth import get_user_model
from channels.testing import WebsocketCommunicator
from django.urls import path
from channels.routing import URLRouter
from channels.db import database_sync_to_async
import logging
import chess
from channels.layers import get_channel_layer

User = get_user_model()
application = URLRouter([
    path("ws/play/<int:gameID>/", ChessConsumer.as_asgi()),
])


class ChessConsumerTests(ChannelsLiveServerTestCase):
    """Test the chess consumer"""
    def setUp(self):
        self.white_user = User.objects.create_user(
            username='white', password='testpassword')
        self.black_user = User.objects.create_user(
            username='black', password='testpassword')
        self.white_token, _ = Token.objects.get_or_create(
            user=self.white_user)
        self.black_token, _ = Token.objects.get_or_create(
            user=self.black_user)
        self.white_token.save()
        self.black_token.save()

        self.white_token_key = self.white_token.key
        self.black_token_key = self.black_token.key

        self.game = ChessGame.objects.create(
            whitePlayer=self.white_user)
        self.game.save()  # single player
        self.game2 = ChessGame.objects.create(
            whitePlayer=self.white_user,
            blackPlayer=self.black_user,
            status='active')
        self.game2.save()  # two players

    async def connect_and_verify(self, gameID, token_key):
        communicator = WebsocketCommunicator(
            application, f"/ws/play/{gameID}/?{token_key}")
        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)
        response = await communicator.receive_json_from()
        return response, communicator

    async def test_000_chess_consumer_connect(self):
        """Test that the consumer is able to connect to the websocket"""
        self.gameID = self.game.id  # Valid game ID
        response, communicator = await self.connect_and_verify(
            self.gameID,
            self.white_token_key)
        self.assertEqual(response["type"], "game")
        self.assertEqual(response["message"], "OK")

        await communicator.disconnect()

    