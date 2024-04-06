from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from rest_framework.authtoken.models import Token
from .models import ChessGame, ChessMove
import json
import chess
from urllib.parse import parse_qs

class ChessConsumer(AsyncWebsocketConsumer):
	room_group_name = str(12345) 

	async def connect(self):
		self.gameID = self.scope['url_route']['kwargs']['gameID']
		
		token_key = 0
		for header in self.scope['headers']:
			if header[0].decode('utf-8').lower() == 'authorization':
				token_key = header[1].decode('utf-8')
				break
		
		if token_key is not None:
			user = await self.get_user_from_token(token_key)
		if not user:
			await self.game_cb("Invalid token. Connection not authorized.", '', 0, error=True)
			await self.close()
			return

		game = await self.get_game(self.gameID)
		if not game:
			await self.game_cb(f"Invalid game with id {self.gameID}", '', user.id, error=True)
			await self.close()
			return
		
		if user and game:
			self.room_group_name = str(self.gameID)
			await self.channel_layer.group_add(
				self.room_group_name,
				self.channel_name
			)
			await self.accept()
			await self.game_cb('OK', game.status, user.id)
			await self.update_active(game)


	async def receive(self, text_data):
		text_data_json = json.loads(text_data)
		message = text_data_json.get('type')
		
		if message == 'move':
			await self.handle_move(text_data_json)

	async def disconnect(self, close_code):
		await self.channel_layer.group_discard(
			self.room_group_name,
			self.channel_name
		)

	async def game_cb(self, message, status, player_id, error=False):
		try:
			msg_type = 'error' if error else 'game'
			await self.channel_layer.group_send(
				self.room_group_name,
				{
					'type': 'game',
					'message': {
						'type': msg_type,
						'message': message,
						'status': status,
						'player_id': player_id,
					}
				}
			)
		except Exception as e:
			print(e)

	async def move_cb(self, from_square, to_square, player_id, promotion='', error=False):
		msg_type = 'error' if error else 'move'
		try:
			await self.channel_layer.group_send(
				self.room_group_name,
				{
					'type': 'move',
					'message': {
						'type': msg_type,
						'from': from_square,
						'to': to_square,
						'playerID': player_id,
						'promotion': promotion,
					}
				}
			)
		except Exception as e:
			print(e)

	async def game_message(self, event):
		await self.send(text_data=json.dumps(event['message']))

	async def move_message(self, event):
		await self.send(text_data=json.dumps(event['message']))

	async def handle_move(self, data):
		try:
			movestr = data.get('message')
			game = await self.get_game(self.gameID)
			token_key = None
			for header in self.scope['headers']:
				if header[0].decode('utf-8').lower() == 'authorization':
					token_key = header[1].decode('utf-8')
					break
			player = await self.get_user_from_token(token_key)

			if game.status != 'active':
				raise ValueError("La partida no está activa.")

			board = chess.Board(game.board_state)
			from_square_index = chess.parse_square(movestr[0] + movestr[1])
			to_square_index = chess.parse_square(movestr[2] + movestr[3])

			move = chess.Move(from_square_index, to_square_index)

			if not board.is_legal(move):
				raise ValueError("Movimiento ilegal.")

			await self.save_chess_move(game, player, movestr[0] + movestr[1], movestr[2] + movestr[3], '')

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
			await self.move_cb(data.get('message'), from_square_index, to_square_index, player.id)
		except ValueError as e:
			print(e)
			await self.move_cb(data.get('message'), from_square_index, to_square_index, player.id, error=True)

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
		
	async def game(self, event):
		message = event['message']
		await self.send(text_data=json.dumps(message))

	async def move(self, event):
		message = event['message']
		await self.send(text_data=json.dumps(message))