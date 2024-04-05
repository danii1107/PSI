from djoser.views import TokenCreateView
from djoser.conf import settings
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from django.db.models import Q
import random
from .models import ChessGame
from .serializers import ChessGameSerializer

class MyTokenCreateView(TokenCreateView):
    def _action(self, serializer):
        response = super()._action(serializer)
        token_string = response.data['auth_token']
        token_object = settings.TOKEN_MODEL.objects.get(key=token_string)
        response.data['user_id'] = token_object.user.id
        response.data['rating'] = token_object.user.rating
        return response

class ChessGameViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = ChessGame.objects.all()
    serializer_class = ChessGameSerializer
    
    def create(self, request, *args, **kwargs):
        try:
            pending_or_active_game = ChessGame.objects.get(
                (Q(whitePlayer__isnull=True) | Q(blackPlayer__isnull=True)) & ~Q(status=ChessGame.FINISHED),
                status__in=[ChessGame.PENDING, ChessGame.ACTIVE]
            )
            if pending_or_active_game.status == ChessGame.ACTIVE:
                return Response({"detail": "Cannot join an active game."}, status=status.HTTP_400_BAD_REQUEST)

            if pending_or_active_game.whitePlayer and pending_or_active_game.whitePlayer != request.user:
                pending_or_active_game.blackPlayer = request.user
            elif pending_or_active_game.blackPlayer and pending_or_active_game.blackPlayer != request.user:
                pending_or_active_game.whitePlayer = request.user
            else:
                return Response({"detail": "Invalid game state."}, status=status.HTTP_400_BAD_REQUEST)

            pending_or_active_game.save()
            serializer = self.get_serializer(pending_or_active_game)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ChessGame.DoesNotExist:
            data = {'whitePlayer': request.user.id} if random.choice([True, False]) else {'blackPlayer': request.user.id}
            serializer = self.get_serializer(data=data)
            if serializer.is_valid(raise_exception=True):
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        game = self.get_object()
        serializer = self.get_serializer(game, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

