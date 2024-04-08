from django.test import TestCase
from models.models import ChessGame, Player
from models.serializers import ChessGameSerializer
from django.utils import timezone


class ChessGameSerializerTest(TestCase):
    def setUp(self):
        self.player1 = Player.objects.create(username='player1', rating=1200)
        self.player2 = Player.objects.create(username='player2', rating=1300)
        self.game = ChessGame.objects.create(
            status=ChessGame.ACTIVE,
            board_state='initial_state',
            start_time=timezone.now(),
            timeControl='10+0',
            blackPlayer=self.player1,
            whitePlayer=self.player2
        )

    def test_serialization(self):
        serializer = ChessGameSerializer(instance=self.game)
        serialized_data = serializer.data

        self.assertEqual(serialized_data['status'], self.game.status)
        self.assertEqual(serialized_data['board_state'], self.game.board_state)
        self.assertEqual(
            serialized_data['start_time'].replace('Z', ''),
            self.game.start_time.replace(tzinfo=None).isoformat()
        )
        self.assertEqual(serialized_data['timeControl'], self.game.timeControl)
        self.assertEqual(
            serialized_data['blackPlayer'],
            self.game.blackPlayer.id
        )
        self.assertEqual(
            serialized_data['whitePlayer'],
            self.game.whitePlayer.id
        )
