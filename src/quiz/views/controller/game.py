from ..common import get_game_by_code
from ..util import parse_bool
from ... import events
from ...models import *
from ...serializers import GameStateSerializer

from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, HttpResponseBadRequest, JsonResponse
from django.urls import reverse


def index(request, game_code: str):
    if request.method == "GET":
        game = get_game_by_code(game_code)
        context = {"game": game}
        return render(request, "controller/game.html", context)


def state(request, game_code: str):
    if request.method == "GET":
        game = get_game_by_code(game_code)
        context = {"game": game}
        return render(request, "controller/game_state.html", context)


def action(request, game_code: str, action: str):
    game = get_game_by_code(game_code)
    if request.method == "POST":
        if action == "next-question":
            if game.question_num >= len(game.cur_round) - 1:
                if game.round_num < len(game.quiz) - 1:
                    game.question_num = 0
                    game.round_num += 1
                    print("Changing to round {game.round_num}")
                else:
                    print("Reached end of quiz")
            else:
                game.question_num += 1
        elif action == "prev-question":
            if game.question_num == 0:
                if game.round_num > 0:
                    game.round_num -= 1
                    game.question_num = len(game.cur_round) - 1
                    print("Changing to round {game.round_num}")
                else:
                    print("Reached start of quiz")
            else:
                game.question_num -= 1
        else:
            return HttpResponseNotFound()

        events.push_question_change()

        game.save()
        serializer = GameStateSerializer(game)
        return JsonResponse(serializer.data)

    return HttpResponseNotFound()


def room(request, game_code: str, room: str = None):
    game = get_game_by_code(game_code)
    prev_room = GameState.Room(game.room)
    if request.method == "POST":
        if room == "lobby":
            game.room = GameState.Room.LOBBY
        elif room == "quiz":
            game.room = GameState.Room.QUIZ
        elif room == "round-end":
            game.room = GameState.Room.ROUND_END
        elif room == "game-end":
            game.room = GameState.Room.GAME_END
        else:
            return HttpResponseNotFound()
        game.save()
        serializer = GameStateSerializer(game)
        events.push_room_change()
        return JsonResponse(serializer.data)

    return HttpResponseNotFound()
