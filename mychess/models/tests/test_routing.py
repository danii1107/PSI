import asyncio
from django.test import TestCase
from channels.testing import WebsocketCommunicator
from models.routing import websocket_urlpatterns
from mychess.models.consumers import GameConsumer

class GameConsumerTestCase(TestCase):
    async def test_game_consumer(self):
        url = "/ws/play/123/token123/"

        communicator = WebsocketCommunicator(websocket_urlpatterns, url)

        connected, _ = await communicator.connect()

        self.assertTrue(connected)

        try:
            await communicator.send_json_to({"type": "hello"})
            response = await communicator.receive_json_from()

            self.assertEqual(response, {"type": "response"})


        finally:
            await communicator.disconnect()
