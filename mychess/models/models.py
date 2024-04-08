"""
Modulo que contiene las clases Player, ChessGame
y ChessMove que son los modelos de la aplicacion
@Autor: Enrique Gomez
"""
import chess
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class Player(AbstractUser):
    """
        Clase representa el modelo jugador
        @Autor: Enrique Gomez
        @atributos: rating: el nivel del jugador
                    created_at: fecha de inicio
                    updated_at: fecha de actualizacion
        @metodos: __str__
    """
    rating = models.IntegerField(default=-1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Player'
        verbose_name_plural = 'Players'

    """
            Metodo que se encarga de pasar el player a string
            @Autor: Enrique Gomez
        """
    def __str__(self):
        return f"{self.username} ({self.rating})"


class ChessGame(models.Model):
    """
    Clase que representa el modelo de una partida de ajedrez
    @Autor: Enrique Gomez
    @atributos: status: estado de la partida
                board_state: estado del tablero en formato FEN
                start_time: fecha y hora de inicio de la partida
                end_time: fecha y hora de finalización de la partida
                timeControl: control de tiempo de la partida
                blackPlayer: jugador con piezas negras
                whitePlayer: jugador con piezas blancas
                winner: jugador ganador de la partida
    @metodos: __str__
    """
    PENDING = 'pending'
    ACTIVE = 'active'
    FINISHED = 'finished'

    STATUS = (
        (PENDING, 'Pending'),
        (ACTIVE, 'Active'),
        (FINISHED, 'Finished'),
    )
    DEFAULT_BOARD_STATE = chess.Board().fen()

    status = models.CharField(max_length=10, choices=STATUS, default='pending')
    board_state = models.CharField(max_length=100, default=DEFAULT_BOARD_STATE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    timeControl = models.CharField(max_length=50)
    blackPlayer = models.ForeignKey(Player, on_delete=models.CASCADE,
                                    related_name='black_games', null=True)
    whitePlayer = models.ForeignKey(Player, on_delete=models.CASCADE,
                                    related_name='white_games', null=True)
    winner = models.ForeignKey(Player, on_delete=models.CASCADE,
                               null=True, blank=True, related_name='won_games')

    def __str__(self):
        """
        Método que devuelve la partida en forma de string
        @Autor: Enrique Gomez
        """
        white_Player = self.whitePlayer if self.whitePlayer else 'unknown'
        black_Player = self.blackPlayer if self.blackPlayer else 'unknown'
        return f'GameID=({self.id}) {white_Player} vs {black_Player}'


class ChessMove(models.Model):
    """
    Clase que representa el modelo de un movimiento en ajedrez
    @Autor: Enrique Gomez
    @atributos: game: partida a la que pertenece el movimiento
                player: jugador que realiza el movimiento
                move_from: casilla de origen del movimiento
                move_to: casilla de destino del movimiento
                promotion: pieza a la que se promociona el peón
    @metodos: __str__, save
    """
    game = models.ForeignKey(ChessGame, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    move_from = models.CharField(max_length=2)
    move_to = models.CharField(max_length=2)
    promotion = models.CharField(max_length=1,
                                 blank=True,
                                 null=True,
                                 default='')

    def __str__(self):
        """
        Método que devuelve el movimiento en forma de string
        @Autor: Enrique Gomez
        """
        move_description = f"{self.move_from} -> {self.move_to}"
        if self.promotion:
            promotion_piece = self.promotion.lower()
            move_description += f" (Promoción a {promotion_piece})"
        return f"{self.player}: {move_description}"

    def save(self, *args, **kwargs):
        """
        Método para guardar el movimiento y
        actualizar el estado del juego
        @Autor: Enrique Gomez
        """
        chess_game = self.game

        if chess_game.status != 'active':
            raise ValueError("La partida no está activa.")

        board = chess.Board(chess_game.board_state)
        from_square = chess.parse_square(self.move_from)
        to_square = chess.parse_square(self.move_to)

        if self.promotion:
            move = chess.Move.from_uci(
                self.move_from + self.move_to + self.promotion
            )
        else:
            move = chess.Move(from_square, to_square)

        if not board.is_legal(move):
            raise ValueError("Movimiento no válido.")

        board.push(move)

        check = board.is_check()
        checkmate = board.is_checkmate()
        draw = (board.is_stalemate() or
                board.is_insufficient_material() or
                board.is_fivefold_repetition() or
                board.can_claim_draw())
        if checkmate:
            chess_game.status = ChessGame.FINISHED
            chess_game.winner = self.player
            chess_game.end_time = timezone.now()
        elif draw:
            chess_game.status = ChessGame.FINISHED
            chess_game.end_time = timezone.now()
        elif check:
            chess_game.status = ChessGame.ACTIVE

        chess_game.board_state = board.fen()
        chess_game.save()

        super().save(*args, **kwargs)
