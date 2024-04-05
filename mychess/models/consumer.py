from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from rest_framework.authtoken.models import Token
from .models import ChessGame, ChessMove
from django.db import models
import json
import chess

class GameConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.gameID = self.scope['url_route']['kwargs']['gameID']
		token_key = self.scope['url_route']['kwargs']['token']

		user = await self.get_user_from_token(token_key)
		game = await self.get_game(self.gameID)
		if user and game:
			self.room_group_name = self.gameID

			await self.channel_layer.group_add(
				self.room_group_name,
				self.channel_name
			)

			await self.accept()
			await self.update_active(game)
			await self.game_cb('Bienvenido a la partida.', 'active', user.id)
		else:
			await self.send(text_data=json.dumps({
				'error': 'Invalid token. Connection closed.'
			}))
			await self.close()

	async def receive(self, text_data):
		text_data_json = json.loads(text_data)
		message = text_data_json.get('type')
		
		if message == 'move':
			await self.handle_move(text_data_json)
			await self.move_cb(text_data_json.get('move'))

	async def disconnect(self, close_code):
		await self.channel_layer.group_discard(
			self.room_group_name,
			self.channel_name
		)

	async def game_cb(self, message, status, player_id, error=False):
		msg_type = 'error' if error else 'game'
		await self.channel_layer.group_send(
			self.room_group_name,
			{
				'type': 'game.message',
				'message': {
					'type': msg_type,
					'message': message,
					'status': status,
					'player_id': player_id,
				}
			}
		)

	async def move_cb(self, from_square, to_square, player_id, promotion='', error=False):
		msg_type = 'error' if error else 'move'
		await self.channel_layer.group_send(
			self.room_group_name,
			{
				'type': 'move.message',
				'message': {
					'type': msg_type,
					'from': from_square,
					'to': to_square,
					'playerID': player_id,
					'promotion': promotion,
				}
			}
		)

	async def game_message(self, event):
		await self.send(text_data=json.dumps(event['message']))

	async def move_message(self, event):
		await self.send(text_data=json.dumps(event['message']))

	async def handle_move(self, data):
		movestr = data.get('move')
		game = await self.get_game(self.gameID)
		player = await self.get_user_from_token(self.scope['url_route']['kwargs']['token'])

		if game.status != 'active':
			raise ValueError("La partida no está activa.")

		board = chess.Board(game.board_state)
		from_square = chess.parse_square(movestr[:1])
		to_square = chess.parse_square(movestr[2:])

		move = chess.Move(from_square, to_square)

		if not board.is_legal(move):
			raise ValueError("Movimiento no válido.")

		await self.save_chess_move(game, player, movestr[:1], movestr[2:], '')

		board.push(move)

		checkmate = board.is_checkmate()
		draw = board.is_stalemate() or board.is_insufficient_material() or board.is_fivefold_repetition() or board.can_claim_draw()

		if checkmate or draw:
			game.status = ChessGame.FINISHED
			if checkmate:
				game.winner = player
			await self.update_game_status(game, board.fen())

		await self.channel_layer.group_send(
			self.room_group_name,
			{
				'type': 'chat_message',
				'message': movestr,
			}
		)

	@database_sync_to_async
	def get_game(self, game_id):
		return ChessGame.objects.get(id=game_id)

	@database_sync_to_async
	def save_chess_move(self, game, player, move_from, move_to, promotion):
		ChessMove.objects.create(
			game=game,
			player=player,
			move_from=move_from,
			move_to=move_to,
			promotion=promotion
		)

	@database_sync_to_async
	def update_game_status(self, game, board_state):
		game.board_state = board_state
		game.save()

	@database_sync_to_async
	def update_active(self, game):
		game.status = ChessGame.ACTIVE
		game.save()

	@database_sync_to_async
	def get_user_from_token(self, token_key):
		try:
			token = Token.objects.get(key=token_key)
			return token.user
		except Token.DoesNotExist:
			return None