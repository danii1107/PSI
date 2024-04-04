from djoser.views import TokenCreateView
from djoser.conf import settings
from rest_framework import mixins, viewsets
import random
from models.models import ChessGame

class MyTokenCreateView(TokenCreateView):
    def _action(self, serializer):
        response = super()._action(serializer)
        token_string = response.data['auth_token']
        token_object = settings.TOKEN_MODEL.objects.get(key=token_string)
        response.data['user_id'] = token_object.user.id
        response.data['rating'] = token_object.user.rating
        return response

class ChessGameViewSet(mixins.CreateModelMixin,
                       mixins.UpdateModelMixin,
                       viewsets.GenericViewSet):
    queryset = ChessGame.objects.all()
    #serializer_class = ChessGameSerializer

    def create(self, request, *args, **kwargs):

        for games in pending_games:
            if game.whitePlayer is None or game.blackPlayer is None:
                if game.status != 'pending':
                    game.delete()
                    raise ValueError("Error")
                return self.update(request, game_id=game.id, *args, **kwargs)
                
            
        for games in queryset:
            if game.whitePlayer is None or game.blackPlayer is None:
                return self.update(game, request.user)
        
        if random.randint(0, 1) == 0:
            black_player= request.user
            white_player = null
        else:
            black_player = null
            white_player = request.user

        new_game = ChessGame.objects.create(
            status='pending',
            whitePlayer=white_player,
            blackPlayer=black_player
        )

        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        game_id = kwargs.get('game_id')
        game = ChessGame.objects.get(id=game_id)
        game.status = 'active'

        if game.whitePlayer is None:
            game.whitePlayer = request.user
        if game.blackPlayer is None:
            blackPlayer = request.user
        
        game.save()

        return super().update(request, *args, **kwargs)
