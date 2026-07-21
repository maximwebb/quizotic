from . import lobby, question
from .common import get_cur_game_state
from ..models import GameState

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound

import json
import os


def quiz_view(request, game_code: int):
    gs = get_cur_game_state(request)
    context = {}

    match gs.room:
        case GameState.Room.LOBBY:
            return lobby.lobby_view(request)
        case GameState.Room.QUIZ:
            return question.question_view(request)
        case _:
            return HttpResponseNotFound()
