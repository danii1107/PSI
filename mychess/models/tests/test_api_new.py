from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
# from django.contrib.auth.models import User
from models.models import ChessGame
from django.contrib.auth import get_user_model
from django.urls import reverse


# you may modify the following lines
URL = '/api/v1/games/'
# do not modify the code below

User = get_user_model()


class ChessGameViewSetTest(TestCase):
    def setUp(self):
        ChessGame.objects.all().delete()
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            username='user1', password='testpassword')
        self.user2 = User.objects.create_user(
            username='user2', password='testpassword')

    def test_create_game_random(self):
        """Create a new game """
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(URL, {})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ChessGame.objects.count(), 1)
        chessgame = ChessGame.objects.first()
        result = (chessgame.whitePlayer == self.user1) or (
            chessgame.blackPlayer == self.user1) 
        self.assertTrue(result)
        if (chessgame.whitePlayer == self.user1):
            while(1):
                ChessGame.objects.all().delete()
                self.client.force_authenticate(user=self.user1)
                response = self.client.post(URL, {})
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)
                self.assertEqual(ChessGame.objects.count(), 1)
                chessgame = ChessGame.objects.first()
                if (chessgame.blackPlayer == self.user1):
                    result = (chessgame.blackPlayer == self.user1)
                    self.assertTrue(result)
                    break
        else:
            while(1):
                ChessGame.objects.all().delete()
                self.client.force_authenticate(user=self.user1)
                response = self.client.post(URL, {})
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)
                self.assertEqual(ChessGame.objects.count(), 1)
                chessgame = ChessGame.objects.first()
                if (chessgame.whitePlayer == self.user1):
                    result = (chessgame.whitePlayer == self.user1)
                    self.assertTrue(result)
                    break



    def test_list(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get('/api/v1/games/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve(self):
        self.game = ChessGame.objects.create(status='active')
        self.url = reverse('games-detail', kwargs={'pk': self.game.pk})
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['id'], self.game.pk)
        self.assertEqual(response.data['status'], self.game.status)

    def test_create_pending_no_users(self):
        ChessGame.objects.all().delete()
        game = ChessGame.objects.create(
            status=ChessGame.PENDING)
        game.save()
        self.client.force_authenticate(user=self.user2)
        response = self.client.post(f'{URL}', {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
