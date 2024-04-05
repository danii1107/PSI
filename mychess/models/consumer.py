from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from rest_framework.authtoken.models import Token
import json
import chess

class GameConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.gameID = self.scope['url_route']['kwargs']['gameID']
		token_key = self.scope['url_route']['kwargs']['token']

		user = await self.get_user_from_token(token_key)
		if user:
			self.room_group_name = self.gameID

			await self.channel_layer.group_add(
				self.room_group_name,
				self.channel_name
			)

			await self.accept()
		else:
			await self.send(text_data=json.dumps({
				'error': 'Invalid token. Connection closed.'
			}))
			await self.close()

	@database_sync_to_async
	def get_user_from_token(self, token_key):
		try:
			token = Token.objects.get(key=token_key)
			return token.user
		except Token.DoesNotExist:
			return None

	async def receive(self, text_data):
		text_data_json = json.loads(text_data)
		message = text_data_json.get('type')

		if message == 'move':
			await self.handle_move(text_data_json)

	async def handle_move(self, data):
		move = data.get('move')
		


	async def chat_message(self, event):
		message = event['message']

		await self.send(text_data=json.dumps({
			'message': message
		}))