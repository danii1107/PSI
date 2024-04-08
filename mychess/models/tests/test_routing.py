from channels.testing import WebsocketCommunicator
from channels.routing import URLRouter
from rest_framework.authtoken.models import Token
from models.models import ChessGame
from django.urls import path
from django.contrib.auth import get_user_model
from models.consumers import ChessConsumer
from channels.testing import ChannelsLiveServerTestCase

User = get_user_model()
application = URLRouter([
    path("ws/play/<int:gameID>/", ChessConsumer.as_asgi()),
])


class ChessRoutingTests(ChannelsLiveServerTestCase):
    """
        Prueba que la expresion regular del routing funciona correctamente
    """
    def setUp(self):
        self.white_user = User.objects.create_user(
            username='white', password='testpassword')
        self.white_token, _ = Token.objects.get_or_create(
            user=self.white_user)
        self.white_token.save()
        self.key = self.white_token.key

        self.game = ChessGame.objects.create(
            whitePlayer=self.white_user)
        self.game.save()  # single player

    async def test_000_chess_consumer_connection(self):
        gameID = self.game.id
        token_key = self.key
        re_path = f'/ws/play/{gameID}/?token={token_key}'
        communicator = WebsocketCommunicator(application, re_path)

        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        await communicator.disconnect()
