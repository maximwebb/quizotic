from . import lobby, question, scoring
from .common import get_game_by_code
from ..models import GameState

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound

def presenter_view(request, game_code: str):
    game = get_game_by_code(game_code)
    match game.room:
        case GameState.Room.LOBBY:
            return presenter_lobby(request, game_code)
        case _:
            return HttpResponseNotFound()


def presenter_lobby(request, game_code: str):
    context = {}
    context["game_code"] = game_code
    context["game"] = get_game_by_code(game_code)

    return render(request, "presenter/lobby.html", context)
