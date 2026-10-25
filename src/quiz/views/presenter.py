from . import lobby, question, scoring
from .common import get_game_by_code, get_cur_question_by_code
from ..models import *

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound


def presenter_view(request, game_code: str):
    game = get_game_by_code(game_code)
    match game.room:
        case GameState.Room.LOBBY:
            return presenter_lobby(request, game)
        case GameState.Room.QUIZ:
            return presenter_quiz(request, game)
        case _:
            return HttpResponseNotFound()


def presenter_lobby(request, game):
    context = {"game_code": game.code, "game": game}

    return render(request, "presenter/lobby.html", context)


def presenter_quiz(request, game):
    question_type = get_cur_question_by_code(game.code).question_type
    match question_type:
        case Question.Type.MCQ:
            return question.mcq_view(request, game.code, is_presenter=True)
        case Question.Type.TEXTBOX:
            return question.textbox_view(request, game.code, is_presenter=True)
        case Question.Type.VOTE:
            return question.vote_view(request, game.code, is_presenter=True)
        case _:
            return HttpResponseNotFound()
