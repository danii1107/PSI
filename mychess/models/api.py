from djoser.views import TokenCreateView
from djoser.conf import settings

class MyTokenCreateView(TokenCreateView):
    def _action(self, serializer):
        response = super()._action(serializer)
        token_string = response.data['auth_token']
        token_object = settings.TOKEN_MODEL.objects.get(key=token_string)
        response.data['user_id'] = token_object.user.id
        response.data['rating'] = token_object.user.rating
        return response