from django.contrib import admin
from .models import Player, ChessGame, ChessMove

admin.site.register(Player)
admin.site.register(ChessGame)
admin.site.register(ChessMove)

# Register your models here.
