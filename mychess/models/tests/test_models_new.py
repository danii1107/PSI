from django.test import TestCase
from django.contrib.auth import get_user_model
from models.models import Player, ChessGame, ChessMove

User = get_user_model()


class ChessMoveModelTest(TestCase):
    def setUp(self):
        self.player1 = Player.objects.create(username='player1', rating=1500)
        self.player2 = Player.objects.create(username='player2', rating=1600)
        self.game = ChessGame.objects.create(
            whitePlayer=self.player1,
            blackPlayer=self.player2,
            status='active',
            board_state=ChessGame.DEFAULT_BOARD_STATE,
            timeControl='10+5'
        )

    def test_001_chessmove_str_method(self):
        fen = "rnbqkbnr/Pppppppp/p7/8/8/8/PPP1PPPP/RNBQKBNR w KQkq - 0 1"
        self.game.board_state = fen
        self.game.save()
        move = ChessMove(
            game=self.game,
            player=self.player1,
            move_from='a7',
            move_to='b8',
            promotion='q'
        )
        self.assertEqual(
            str(move),
            'player1 (1500): a7 -> b8 (Promoción a q)'
        )

    def test_checkmate(self):
        fen = "3k4/8/3K4/8/8/8/8/6R1 w - - 0 1"
        self.game.board_state = fen
        self.game.save()

        ChessMove.objects.create(
            game=self.game,
            player=self.player1,
            move_from='g1',
            move_to='g8'
        )

        self.assertEqual(self.game.status, ChessGame.FINISHED)

        self.assertEqual(self.game.winner, self.player1)

    def test_checkdraw(self):
        fen = "8/8/8/8/8/5k2/4K3/8 w - - 0 1"
        self.game.board_state = fen
        self.game.save()
        ChessMove.objects.create(
            game=self.game,
            player=self.player1,
            move_from='e2',
            move_to='e1'
        )

        self.assertEqual(self.game.status, ChessGame.FINISHED)

        self.assertEqual(self.game.winner, None)

    def test_continue(self):
        self.game.board_state = "8/8/8/8/8/4k3/8/4K2R w - - 0 1"
        self.game.save()
        move = ChessMove(
            game=self.game,
            player=self.player1,
            move_from='h1',
            move_to='h3'
        )
        move.save()

        self.assertEqual(self.game.status, ChessGame.ACTIVE)
