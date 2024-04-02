import chess

from django.db import models
from django.contrib.auth.models import AbstractUser

class Player(AbstractUser):
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Player'
        verbose_name_plural = 'Players'

    def __str__(self):
        return self.username

class ChessGame(models.Model):
    STATUS = (
    ('pending', 'pending'),
    ('active', 'active'),
    ('finished', 'finished'),
)

    status = models.CharField(max_length=10, choices=STATUS, default='pending')
    board_state = models.CharField(max_length=100)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    timeControl = models.CharField(max_length=50)
    blackPlayer = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='black_games')
    whitePlayer = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='white_games')
    winner = models.ForeignKey(Player, on_delete=models.CASCADE, null=True, blank=True, related_name='won_games')

    def __str__(self):
        return f"Partida de Ajedrez entre {self.white_player.username} (Blancas) y {self.black_player.username} (Negras)"

class ChessMove(models.Model):
    game = models.ForeignKey(ChessGame, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    move_from = models.CharField(max_length=2)
    move_to = models.CharField(max_length=2)
    promotion = models.CharField(max_length=1, blank=True, null=True)

    def __str__(self):
        player_color = "Blancas" if self.player == self.game.white_player else "Negras"
        move_description = f"{self.move_from} -> {self.move_to}"
        if self.promotion:
            promotion_piece = self.promotion.lower()
            move_description += f" (Promoción a {promotion_piece})"
        return f"Jugador: {self.player.username} ({player_color}), Movimiento: {move_description}"

    def save(self, *args, **kwargs):
        chess_game = self.game

        if chess_game.status != 'active':
            raise ValueError("La partida no está activa.")

        board = chess.Board(chess_game.board_state)
        from_square = chess.parse_square(self.move_from)
        to_square = chess.parse_square(self.move_to)
        move = chess.Move(from_square, to_square)
        if move not in board.legal_moves:
            raise ValueError("Movimiento no válido.")
        board.push(move)
        chess_game.board_state = board.fen()
        chess_game.save()

        super().save(*args, **kwargs)

