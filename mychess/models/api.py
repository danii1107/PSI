"""
    Módulo que contiene las vistas de la API de MyChess.
    @autor: Daniel Birsan y Enrique Gómez Fernández
"""

from djoser.views import TokenCreateView
from djoser.conf import settings
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from django.db.models import Q
import random
from .models import ChessGame
from .serializers import ChessGameSerializer


class MyTokenCreateView(TokenCreateView):
    """
        Clase que extiende la vista de creación de token de Djoser
        para añadir el rating y el id del usuario al response.
        @autor: Enrique Gómez Fernández
        @metodos: _action
    """
    def _action(self, serializer):
        """
            Método que añade el rating y el id del usuario al response.
            @autor: Enrique Gómez Fernández
            @param serializer: Serializador de la vista.
            @return: Response con el rating y el id del usuario.
        """
        response = super()._action(serializer)
        token_string = response.data['auth_token']
        token_object = settings.TOKEN_MODEL.objects.get(key=token_string)
        response.data['user_id'] = token_object.user.id
        response.data['rating'] = token_object.user.rating
        return response


class ChessGameViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    """
        Clase que extiende la vista de creación de token de Djoser
        para añadir el rating y el id del usuario al response.
        @autor: Daniel Birsan
        @atributos: queryset; almacenamiento de los objetos de la base de datos
                serializer_class; serializador de la clase
        @metodos: create, update, list, retrieve
    """
    queryset = ChessGame.objects.all()
    serializer_class = ChessGameSerializer

    def create(self, request, *args, **kwargs):
        """
            Método que crea una partida de ajedrez.
            @autor: Daniel Birsan
            @param request: petición
            @return: Response con la partida de ajedrez creada.
        """
        try:
            # Buscar una partida pendiente o activa
            pending_or_active_game = ChessGame.objects.get(
                (Q(whitePlayer__isnull=True) | Q(blackPlayer__isnull=True)) &
                ~Q(status=ChessGame.FINISHED),
                status__in=[ChessGame.PENDING, ChessGame.ACTIVE]
            )
            # Si la partida está activa o pendiente y no tiene jugadores
            if pending_or_active_game.status == ChessGame.ACTIVE or (
                pending_or_active_game.status == ChessGame.PENDING and
                pending_or_active_game.blackPlayer is None and
                pending_or_active_game.whitePlayer is None
            ):
                return Response(
                    {"detail": "Cannot join an active game."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            # Si la partida está pendiente y tiene un jugador, unirse a ella
            if (pending_or_active_game.whitePlayer is None or
                    pending_or_active_game.blackPlayer is None):
                return self.update(
                    request, game_id=pending_or_active_game.id, *args, **kwargs
                )
        # Si no se ha encontrado ninguna partida disponible, crear una nueva
        except ChessGame.DoesNotExist:
            # Elegir aleatoriamente el color del jugador
            if random.choice([True, False]):
                data = {'whitePlayer': request.user.id}
            else:
                data = {'blackPlayer': request.user.id}
            serializer = self.get_serializer(data=data)
            if serializer.is_valid(raise_exception=True):
                # Crear la partida, serializar y devolverla
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED,
                                headers=headers)

    def update(self, request, *args, **kwargs):
        """
            Método que actualiza una partida de ajedrez.
            @autor: Enrique Gómez Fernández
            @param request: petición
            @return: Response con la partida de ajedrez actualizada.
        """
        game_id = kwargs.get('game_id')
        pending_or_active_game = ChessGame.objects.get(id=game_id)

        # Si el jugador que intenta unirse a la partida no está en ella, unirlo
        if (pending_or_active_game.whitePlayer and
                pending_or_active_game.whitePlayer != request.user):
            pending_or_active_game.blackPlayer = request.user
        elif (pending_or_active_game.blackPlayer and
              pending_or_active_game.blackPlayer != request.user):
            pending_or_active_game.whitePlayer = request.user

        # Guardar los cambios, serializar y devolver la partida
        pending_or_active_game.save()
        serializer = self.get_serializer(pending_or_active_game)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        """
            Método que lista las partidas de ajedrez.
            @autor: Daniel Birsan
            @param request: petición
            @return: Response con las partidas de ajedrez.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        """
            Método que obtiene una partida de ajedrez.
            @autor: Daniel Birsan
            @param request: petición
            @param pk: clave primaria
            @return: Response con la partida de ajedrez.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
