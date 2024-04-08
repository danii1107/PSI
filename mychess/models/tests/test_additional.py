"""
    Este archivo contiene las pruebas unitarias de los modelos y vistas
    para un coverage del 99%.
    @autor: Enrique Gómez Fernández
"""


from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse
from models.models import Player, ChessGame, ChessMove
from channels.testing import WebsocketCommunicator
from channels.routing import URLRouter
from rest_framework.authtoken.models import Token
from django.urls import path
from models.consumers import ChessConsumer
from channels.testing import ChannelsLiveServerTestCase
from models.serializers import ChessGameSerializer
from django.utils import timezone


URL = '/api/v1/games/'

User = get_user_model()

# Define el enrutamiento del WebSocket
application = URLRouter([
    path("ws/play/<int:gameID>/", ChessConsumer.as_asgi()),
])


class ChessGameApiTest1(TestCase):
    """
        Prueba de la API de MyChess. Extiende la clase TestCase de Django.
        @autor: Enrique Gómez Fernández
        @atributos: client; cliente de la API
                user1; usuario 1
                user2; usuario 2
        @metodos: setUp, test_create_game_random, test_list, test_retrieve,
                test_create_pending_no_users
    """
    def setUp(self):
        """
            Método que inicializa las variables de la clase.
            @autor: Enrique Gómez Fernández
        """
        ChessGame.objects.all().delete()
        # Crea un cliente de la API
        self.client = APIClient()
        # Crea dos usuarios
        self.user1 = User.objects.create_user(
            username='user1', password='testpassword')
        self.user2 = User.objects.create_user(
            username='user2', password='testpassword')

    def test_create_game_random(self):
        """
            Método que crea una partida de ajedrez aleatoria.
            @autor: Enrique Gómez Fernández
        """
        # Inicia la sesión del cliente
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(URL, {})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ChessGame.objects.count(), 1)
        chessgame = ChessGame.objects.first()
        # Comprueba que es asignado a uno de los dos jugadores (b o n)
        result = (chessgame.whitePlayer == self.user1) or (
            chessgame.blackPlayer == self.user1)
        self.assertTrue(result)
        # Hace lo mismo para blanco o negro, porque es selección aleatoria
        if (chessgame.whitePlayer == self.user1):
            while (1):
                ChessGame.objects.all().delete()
                self.client.force_authenticate(user=self.user1)
                response = self.client.post(URL, {})
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)
                self.assertEqual(ChessGame.objects.count(), 1)
                chessgame = ChessGame.objects.first()
                if (chessgame.blackPlayer == self.user1):
                    # Comprueba que es negro
                    result = (chessgame.blackPlayer == self.user1)
                    self.assertTrue(result)
                    break
        else:
            while (1):
                ChessGame.objects.all().delete()
                self.client.force_authenticate(user=self.user1)
                response = self.client.post(URL, {})
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)
                self.assertEqual(ChessGame.objects.count(), 1)
                chessgame = ChessGame.objects.first()
                if (chessgame.whitePlayer == self.user1):
                    # Comprueba que es blanco
                    result = (chessgame.whitePlayer == self.user1)
                    self.assertTrue(result)
                    break

    def test_list(self):
        """
            Metodo que prueba el get de las partidas
            @autor: Enrique Gómez Fernández
        """
        self.client.force_authenticate(user=self.user1)
        response = self.client.get('/api/v1/games/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve(self):
        """
            Método que prueba el get de una partida
            @autor: Enrique Gómez Fernández
        """
        self.game = ChessGame.objects.create(status='active')
        self.url = reverse('games-detail', kwargs={'pk': self.game.pk})
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['id'], self.game.pk)
        self.assertEqual(response.data['status'], self.game.status)

    def test_create_pending_no_users(self):
        """
            Método que prueba la creación de una partida pendiente sin usuarios
            @autor: Enrique Gómez Fernández
        """
        ChessGame.objects.all().delete()
        game = ChessGame.objects.create(
            status=ChessGame.PENDING)
        game.save()
        self.client.force_authenticate(user=self.user2)
        response = self.client.post(f'{URL}', {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ChessMoveModelTest1(TestCase):
    """
        Prueba del modelo ChessMove. Extiende la clase TestCase de Django.
        @autor: Enrique Gómez Fernández
        @atributos: player1; jugador 1
                player2; jugador 2
                game; partida
                move; movimiento
        @metodos: setUp, test_chessmove_str_method, test_checkmate,
                test_checkdraw, test_continue
    """
    def setUp(self):
        """
            Método que inicializa las variables de la clase.
            @autor: Enrique Gómez Fernández
        """
        self.player1 = Player.objects.create(username='player1', rating=1500)
        self.player2 = Player.objects.create(username='player2', rating=1600)
        self.game = ChessGame.objects.create(
            whitePlayer=self.player1,
            blackPlayer=self.player2,
            status='active',
            board_state=ChessGame.DEFAULT_BOARD_STATE,
            timeControl='10+5'
        )

    def test_chessmove_str_method(self):
        """
            Método que prueba el método __str__ del modelo ChessMove.
            @autor: Enrique Gómez Fernández
        """
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
        """
            Método que prueba el jaque mate.
            @autor: Enrique Gómez Fernández
        """
        # Situación de jaque mate
        fen = "3k4/8/3K4/8/8/8/8/6R1 w - - 0 1"
        self.game.board_state = fen
        self.game.save()

        ChessMove.objects.create(
            game=self.game,
            player=self.player1,
            move_from='g1',
            move_to='g8'
        )

        # Comprueba que la partida ha terminado
        self.assertEqual(self.game.status, ChessGame.FINISHED)
        # Comprueba que el jugador 1 ha ganado
        self.assertEqual(self.game.winner, self.player1)

    def test_checkdraw(self):
        """
            Método que prueba el empate.
            @autor: Enrique Gómez Fernández
        """
        fen = "8/8/8/8/8/5k2/4K3/8 w - - 0 1"
        self.game.board_state = fen
        self.game.save()
        ChessMove.objects.create(
            game=self.game,
            player=self.player1,
            move_from='e2',
            move_to='e1'
        )

        # Comprueba que la partida ha terminado
        self.assertEqual(self.game.status, ChessGame.FINISHED)
        # Comprueba que no hay ganador
        self.assertEqual(self.game.winner, None)

    def test_continue(self):
        """
            Método que prueba que la partida sigue activa,
            después de un movimiento.
        """
        self.game.board_state = "8/8/8/8/8/4k3/8/4K2R w - - 0 1"
        self.game.save()
        move = ChessMove(
            game=self.game,
            player=self.player1,
            move_from='h1',
            move_to='h3'
        )
        # Guarda el movimiento
        move.save()
        # Comprueba que la partida sigue activa
        self.assertEqual(self.game.status, ChessGame.ACTIVE)


class ChessRoutingTests(ChannelsLiveServerTestCase):
    """
        Prueba de enrutamiento de WebSocket. Extiende la clase
        ChannelsLiveServerTestCase de Django.
        @autor: Daniel Birsan
        @atributos: white_user; usuario blanco
                white_token; token del usuario blanco
                key; clave del token
                game; partida
        @metodos: setUp, test_chess_consumer_connection
    """
    def setUp(self):
        """
            Método que inicializa las variables de la clase.
            @autor: Daniel Birsan
        """
        self.white_user = User.objects.create_user(
            username='white', password='testpassword')
        self.white_token, _ = Token.objects.get_or_create(
            user=self.white_user)
        self.white_token.save()
        self.key = self.white_token.key

        self.game = ChessGame.objects.create(
            whitePlayer=self.white_user)
        self.game.save()

    async def test_chess_consumer_connection(self):
        """
            Método que prueba la conexión del consumidor de ajedrez.
            @autor: Daniel Birsan
        """
        gameID = self.game.id
        token_key = self.key
        # Expresión regular para la URL del WebSocket
        re_path = f'/ws/play/{gameID}/?token={token_key}'
        communicator = WebsocketCommunicator(application, re_path)

        connected, _ = await communicator.connect()
        # Comprueba que la conexión se ha establecido
        self.assertTrue(connected)

        await communicator.disconnect()


class ChessGameSerializerTest(TestCase):
    """
        Prueba del serializador ChessGameSerializer.
        Extiende la clase TestCase de Django.
        @autor: Enrique Gómez Fernández
        @atributos: player1; jugador 1
                player2; jugador 2
                game; partida
        @metodos: setUp, test_serialization
    """
    def setUp(self):
        """
            Método que inicializa las variables de la clase.
            @autor: Enrique Gómez Fernández
        """
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
        """
            Método que prueba la serialización de una partida.
            @autor: Enrique Gómez Fernández
        """
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


class ChessGameViewSetTest(TestCase):
    """
        Prueba del viewset ChessGameViewSet.
        Extiende la clase TestCase de Django.
        @autor: Enrique Gómez Fernández
        @atributos: client; cliente de la API
                user; usuario
                game; partida
                token; token del usuario
        @metodos: setUp, test_view
    """
    def setUp(self):
        """
            Método que inicializa las variables de la clase.
            @autor: Enrique Gómez Fernández
        """
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='12345'
        )
        self.game = ChessGame.objects.create(
            status=ChessGame.ACTIVE,
            board_state='initial_state',
            start_time=timezone.now(),
            timeControl='10+0',
            blackPlayer=self.user,
            whitePlayer=self.user
        )
        self.token = Token.objects.create(user=self.user)

    def test_view(self):
        """
            Método que prueba la vista de una partida.
            @autor: Enrique Gómez Fernández
        """
        self.client.force_authenticate(user=self.user)
        # Obtener el gameID de la url
        url = reverse('mychess_template', kwargs={'gameID': self.game.id})
        # Concatenar la url con el token de los argumentos de la petición
        url = url + '?' + self.token.key
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
