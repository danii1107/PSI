"""
Modulo que contiene los serializadores de los modelos
de la aplicacion.
@autor: Daniel Birsan
"""

from rest_framework import serializers
from .models import ChessGame


class ChessGameSerializer(serializers.ModelSerializer):
    """
        Serializador del modelo ChessGame.
        @autor: Daniel Birsan
        @metodos: __init__
    """
    class Meta:
        """
            Clase Meta del serializador.
            @autor: Daniel Birsan
        """
        model = ChessGame
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        """
            Metodo que inicializa el serializador.
            @autor: Daniel Birsan
            @param: *args, **kwargs
        """
        super(ChessGameSerializer, self).__init__(*args, **kwargs)
        # Establece los campos requeridos del modelo ChessGame
        # como no requeridos para cumplir post{}
        for field in self.fields.values():
            field.required = False
