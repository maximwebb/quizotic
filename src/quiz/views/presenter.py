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
        case GameState.Room.ROUND_START:
            return presenter_round_start(request, game)
        case GameState.Room.QUIZ:
            return presenter_quiz(request, game)
        case GameState.Room.SCOREBOARD:
            return presenter_scoreboard(request, game)
        case GameState.Room.GAME_END:
            return presenter_game_end(request, game)
        case _:
            return HttpResponseNotFound()


def presenter_lobby(request, game):
    context = {"game_code": game.code, "game": game}

    return render(request, "presenter/lobby.html", context)


def presenter_round_start(request, game):
    context = {"game": game, "round_name": game.cur_round.name}
    if game.cur_round.image is not None:
        context["image"] = game.cur_round.image

    return render(request, "presenter/round_start.html", context)


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


def presenter_scoreboard(request, game):
    return scoring.scoreboard_view(request, game.code, is_presenter=True)

def presenter_game_end(request, game):
    winner = scoring.get_winning_team(game)
    context = {"game": game, "team": winner}

    return render(request, "presenter/game_end.html", context)
