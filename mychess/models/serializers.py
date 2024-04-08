from rest_framework import serializers
from .models import ChessGame


class ChessGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChessGame
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ChessGameSerializer, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False
