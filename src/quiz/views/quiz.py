from . import lobby, question, scoring
from .common import get_game_by_code
from ..models import GameState

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound

import json
import os


def quiz_view(request, game_code: str):
    gs = get_game_by_code(game_code)
    context = {}

    # TODO: should these pass gs instead of game_code?
    match gs.room:
        case GameState.Room.LOBBY:
            return lobby.lobby_view(request, game_code)
        case GameState.Room.QUIZ:
            return question.question_view(request, game_code)
        case GameState.Room.SCOREBOARD:
            return scoring.scoreboard_view(request, game_code)
        case GameState.Room.ROUND_START:
            context = {"game": gs, "round_name": gs.cur_round.name}
            return render(request, "quiz/round_start.html", context)
        case _:
            print("wut")
            return scoring.scoreboard_view(request, game_code)
