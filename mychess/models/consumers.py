"""
Modulo que contiene la clase ChessConsumer que se
encarga de manejar las conexiones
websocket para el juego de ajedrez.
@Autor: Daniel Birsan
"""

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from rest_framework.authtoken.models import Token
from .models import ChessGame, ChessMove
import json
import chess


class ChessConsumer(AsyncWebsocketConsumer):
    """
        Clase que se encarga de manejar las conexiones websocket.
        Se encarga de manejar los mensajes de los jugadores y
        de enviar mensajes a los jugadores conectados.
        @Autor: Daniel Birsan
        @atributos: room_group_name; Nombre del grupo de la sala,
                    gameID; ID del juego,
        @metodos: connect, receive, disconnect, game_cb, move_cb,
                    handle_move, get_game, save_chess_move,
                    update_game_status, update_finished, get_user_from_token,
                    verify_game, game_message, move_message.
    """
    room_group_name = str(0)

    async def connect(self):
        """
            Metodo que se encarga de aceptar la conexion del
            jugador y de verificar si el token es valido.
            Si el token es valido, se agrega al grupo de la sala.
            @Autor: Daniel Birsan
        """
        # Acepta la conexion para callbacks
        await self.accept()
        # Obtiene el ID del juego de la url
        self.gameID = self.scope['url_route']['kwargs']['gameID']
        # Obtiene el token de los parametros de la petición
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

        # Comprueba si el jugador puede unirse al juego
        cond = await self.verify_game(self.gameID, token_key)
        if cond is False:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': f"Invalid game with id {self.gameID}"
            }))
            await self.close()
            return

        # Agrega al jugador al channel y enviar OK
        self.room_group_name = str(self.gameID)
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.game_cb('OK', game.status, user.id)
        return

    async def receive(self, text_data):
        """
            Metodo que se encarga de recibir los mensajes de los jugadores
            y de manejarlos.
            @Autor: Daniel Birsan
            @param text_data: Mensaje recibido del jugador.
        """
        text_data_json = json.loads(text_data)
        message = text_data_json.get('type')

        if message == 'move':
            await self.handle_move(text_data_json)

    async def disconnect(self, close_code):
        """
            Metodo que se encarga de desconectar al jugador.
            @Autor: Daniel Birsan
            @param close_code: Codigo de cierre de la conexion.
        """
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await super().disconnect(close_code)

    async def game_cb(self, message, status, player_id, error=False):
        """
            Callback para enviar mensajes de estado del juego.
            @Autor: Daniel Birsan
            @param message: Mensaje a enviar.
            @param status: Estado del juego.
            @param player_id: ID del jugador.
            @param error: Bandera de error, false por defecto.
        """
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
        """
            Callback para enviar mensajes de movimiento de fichas.
            @Autor: Daniel Birsan
            @param from_square: Casilla de origen.
            @param to_square: Casilla de destino.
            @param player_id: ID del jugador.
            @param promotion: Promoción de la ficha.
            @param error: Bandera de error, false por defecto.
        """
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

    async def handle_move(self, data):
        """
            Metodo que se encarga de manejar los movimientos de los jugadores.
            @Autor: Daniel Birsan
            @param data: Datos del movimiento.
        """
        from_sq = data.get('from')
        to_sq = data.get('to')
        promotion = data.get('promotion')
        game = await self.get_game(self.gameID)
        token_key = self.scope['query_string'].decode('utf-8')
        if token_key.endswith('/'):
            token_key = token_key[:-1]
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
            await self.update_finished(game, checkmate, player)
            await self.update_game_status(game, board.fen())

        await self.move_cb(from_sq, to_sq, player.id, promotion=promotion)

    @database_sync_to_async
    def get_game(self, game_id):
        """
            Metodo que obtiene el juego con el ID dado.
            @Autor: Daniel Birsan
            @param game_id: ID del juego.
            @return: Juego con el ID dado.
        """
        try:
            game = ChessGame.objects.get(id=game_id)
            return game
        except ChessGame.DoesNotExist:
            return None

    @database_sync_to_async
    def save_chess_move(self, game, player, move_from, move_to, promotion):
        """
            Metodo que guarda el movimiento de una ficha en la base de datos.
            @Autor: Daniel Birsan
            @param game: Juego.
            @param player: Jugador.
            @param move_from: Casilla de origen.
            @param move_to: Casilla de destino.
            @param promotion: Promoción de la ficha.
        """
        ChessMove.objects.create(
            game=game,
            player=player,
            move_from=move_from,
            move_to=move_to,
            promotion=promotion
        )

    @database_sync_to_async
    def update_game_status(self, game, board_state):
        """
            Metodo que actualiza el estado del juego.
            @Autor: Daniel Birsan
            @param game: Juego.
            @param board_state: Estado del tablero.
        """
        game.board_state = board_state
        game.save()

    @database_sync_to_async
    def update_finished(self, game, checkmate, player):
        """
            Metodo que actualiza el estado del juego a finalizado.
            @Autor: Daniel Birsan
            @param game: Juego.
            @param checkmate: Bandera de jaque mate.
            @param player: Jugador ganador.
        """
        game.status = ChessGame.FINISHED
        if checkmate:
            game.winner = player
        game.save()

    @database_sync_to_async
    def get_user_from_token(self, token_key):
        """
            Metodo que obtiene el usuario a partir de un token.
            @Autor: Daniel Birsan
            @param token_key: Token.
            @return: Usuario.
        """
        if token_key.endswith('/'):
            token_key = token_key[:-1]
        try:
            token = Token.objects.get(key=token_key)
            return token.user
        except Token.DoesNotExist:
            return None

    @database_sync_to_async
    def verify_game(self, gameID, token_key):
        """
            Metodo que verifica si el jugador se puede unir.
            @Autor: Daniel Birsan
            @param gameID: ID del juego.
            @param token_key: Token.
            @return: True si puede, False si no.
        """
        game = ChessGame.objects.get(id=gameID)
        if token_key.endswith('/'):
            token_key = token_key[:-1]
        user = Token.objects.get(key=token_key).user
        if game.whitePlayer is not None and game.blackPlayer is not None:
            if game.whitePlayer.id == user.id or\
                    game.blackPlayer.id == user.id:
                self.update_active(game)
                return True
            return False
        if game.whitePlayer is None and game.blackPlayer is None:
            game.whitePlayer = user
            game.save()
            return True
        if game.whitePlayer is not None and game.blackPlayer is None:
            if game.whitePlayer.id == user.id:
                self.update_active(game)
                return True
            return False
        if game.blackPlayer is not None and game.whitePlayer is None:
            if game.blackPlayer.id == user.id:
                self.update_active(game)
                return True
            return False
        return False

    def update_active(self, game):
        """
            Metodo que actualiza el estado del juego a activo.
            @Autor: Daniel Birsan
            @param game: Juego.
        """
        if game.status == ChessGame.PENDING:
            game.status = ChessGame.ACTIVE
            game.save()

    async def game_message(self, event):
        """
            Handler de mensajes de estado del juego.
            @Autor: Daniel Birsan
            @param event: Evento.
        """
        message = event['message']
        await self.send(text_data=json.dumps(message))

    async def move_message(self, event):
        """
            Handler de mensajes de movimiento de fichas.
            @Autor: Daniel Birsan
            @param event: Evento.
        """
        message = event['message']
        await self.send(text_data=json.dumps(message))
