from django.test import TestCase
from models.models import ChessGame, Player
from models.serializers import ChessGameSerializer
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model



User = get_user_model()

class ChessGameSerializerTest(TestCase):
    def setUp(self):  
        ChessGame.objects.all().delete()
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            username='user1', password='testpassword')
        self.user2 = User.objects.create_user(
            username='user2', password='testpassword')
        self.player1 = Player.objects.create(username='player1', rating=1500)
        self.player2 = Player.objects.create(username='player2', rating=1600)
        self.game = ChessGame.objects.create(
            whitePlayer=self.player1,
            blackPlayer=self.player2,
            status='active',
            board_state=ChessGame.DEFAULT_BOARD_STATE,
            timeControl='10+5'
        )

        

        

    def test_serializer_with_valid_data(self):
        serializer = ChessGameSerializer(instance=self.game)
        self.assertTrue(serializer.is_valid())