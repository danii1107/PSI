from channels.testing import WebsocketCommunicator
from channels.routing import URLRouter
from django.test import TestCase
from django.urls import path
from models.consumer import GameConsumer

application = URLRouter([
	path('ws/mychess/<room_name>/', GameConsumer.as_asgi()),
])

class ChatTests1(TestCase):
	async def test_chat(self):
		communicator = WebsocketCommunicator(application, "/ws/mychess/room_name/")
		connected, _ = await communicator.connect()
		self.assertTrue(connected)

		await communicator.send_json_to({
			'message': 'hello',
		})

		response = await communicator.receive_json_from()
		self.assertEqual(response['message'], 'hello')
		await communicator.disconnect()

class ChatTests2(TestCase):
	async def test_chat(self):
		communicator1 = WebsocketCommunicator(application, "/ws/mychess/mychess/")
		communicator2 = WebsocketCommunicator(application, "/ws/mychess/mychess/")

		connected1, _ = await communicator1.connect()
		connected2, _ = await communicator2.connect()
		self.assertTrue(connected1)
		self.assertTrue(connected2)
		
		await communicator1.send_json_to({
			'message': 'hello comm2',
		})

		response1 = await communicator1.receive_json_from()
		self.assertEqual(response1['message'], 'hello comm2')
		response2 = await communicator2.receive_json_from()
		self.assertEqual(response2['message'], 'hello comm2')

		await communicator1.disconnect()
		await communicator2.disconnect()