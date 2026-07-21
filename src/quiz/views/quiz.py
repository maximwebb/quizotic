from . import lobby, question
from .common import get_game_by_code
from ..models import GameState

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound

import json
import os


def quiz_view(request, game_code: str):
    gs = get_game_by_code(game_code)
    context = {}

    print(f"quizview: {gs}")
    match gs.room:
        case GameState.Room.LOBBY:
            print("Going lobby")
            return lobby.lobby_view(request, game_code)
        case GameState.Room.QUIZ:
            print("Going quiz")
            return question.question_view(request, game_code)
        case _:
            return HttpResponseNotFound()
