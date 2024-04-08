from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from rest_framework.authtoken.models import Token
from .models import ChessGame, ChessMove
import json
import chess


class ChessConsumer(AsyncWebsocketConsumer):
    room_group_name = str(0)

    async def connect(self):
        await self.accept()
        self.gameID = self.scope['url_route']['kwargs']['gameID']
        token_key = self.scope['query_string'].decode('utf-8')

        user = await self.get_user_from_token(token_key)
        if user is None:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Invalid token. Connection not authorized.'
            }))
            await self.close()
            return

        game = await self.get_game(self.gameID)
        if game is None:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': f"Invalid game with id {self.gameID}"
            }))
            await self.close()
            return

        cond = await self.verify_game(self.gameID, token_key)
        if cond is True:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': f"Invalid game with id {self.gameID}"
            }))
            await self.close()
            return

        self.room_group_name = str(self.gameID)
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.game_cb('OK', game.status, user.id, False)
        return

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
        await super().disconnect(close_code)

    async def game_cb(self, message, status, player_id, error):
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

    async def move_cb(self, from_square, to_square, player_id,
                      promotion='', error=False):
        msg_type = 'error' if error else 'move'
        try:
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
        except Exception:
            pass

    async def handle_move(self, data):
        try:
            from_sq = data.get('from')
            to_sq = data.get('to')
            promotion = data.get('promotion')
            game = await self.get_game(self.gameID)
            token_key = self.scope['query_string'].decode('utf-8')
            player = await self.get_user_from_token(token_key)

            if game.status != 'active':
                await self.send(text_data=json.dumps({
                    'type': 'error',
                    'message': "Error: invalid move (game is not active)"
                }))
                return

            board = chess.Board(game.board_state)
            from_square_index = chess.parse_square(from_sq)
            to_square_index = chess.parse_square(to_sq)

            if promotion:
                move = chess.Move.from_uci(from_sq + to_sq + promotion)
            else:
                move = chess.Move(from_square_index, to_square_index)

            if not board.is_legal(move):
                await self.send(text_data=json.dumps({
                    'type': 'error',
                    'message': f"Error: invalid move {from_sq}{to_sq}"
                }))
                return

            await self.save_chess_move(game, player, from_sq, to_sq, promotion)

            board.push(move)

            checkmate = board.is_checkmate()
            draw = (board.is_stalemate() or
                    board.is_insufficient_material() or
                    board.is_fivefold_repetition() or
                    board.can_claim_draw())

            if checkmate or draw:
                game.status = ChessGame.FINISHED
                if checkmate:
                    game.winner = player
                await self.update_game_status(game, board.fen())

            await self.move_cb(from_sq, to_sq, player.id, promotion=promotion)
        except ValueError:
            await self.move_cb(from_sq, to_sq, player.id,
                               promotion=promotion, error=True)

    @database_sync_to_async
    def get_game(self, game_id):
        try:
            game = ChessGame.objects.get(id=game_id)
            return game
        except ChessGame.DoesNotExist:
            return None

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

    @database_sync_to_async
    def verify_game(self, gameID, token_key):
        game = ChessGame.objects.get(id=gameID)
        user = Token.objects.get(key=token_key).user
        if game.whitePlayer is not None:
            if game.whitePlayer.id == user.id:
                return False
        if game.blackPlayer is not None:
            if game.blackPlayer.id == user.id:
                return False
        return True

    async def game_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))

    async def move_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))
