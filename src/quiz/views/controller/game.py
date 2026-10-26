from ..common import get_game_by_code
from ..util import parse_bool
from ... import events
from ...models import *
from ...serializers import GameStateSerializer

from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, HttpResponseBadRequest, JsonResponse
from django.urls import reverse

from dataclasses import dataclass, asdict


@dataclass
class GamePos:
    """ Represents the current room/round/question """
    room: GameState.Room
    round: int
    question: int

    def start():
        return GamePos(room=GameState.Room.LOBBY, round=0, question=0)

    def __str__(self):
        return f"{self.room.label} | Round {self.round} | Q{self.question}"


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


def position(request, game_code: str):
    if request.method == "GET":
        game = get_game_by_code(game_code)
        nxt = next_game_pos(game)
        prev = prev_game_pos(game)
        print(nxt)
        print(prev)
        data = {"next": str(nxt), "prev": str(prev)}
        return JsonResponse(data)


# Lobby -> Round Start -> Q1 -> ... -> QN -> Scoreboard -> Game End
#               ^--------------------------------|
def action(request, game_code: str, action: str):
    game = get_game_by_code(game_code)
    if request.method == "POST":
        if action == "next":
            game_pos = next_game_pos(game)
        elif action == "prev":
            game_pos = prev_game_pos(game)
        elif action == "reset":
            game_pos = GamePos.start()
        else:
            return HttpResponseNotFound()

        game.room = game_pos.room
        game.round_num = game_pos.round
        game.question_num = game_pos.question

        events.push_question_change()

        game.save()
        serializer = GameStateSerializer(game)
        return JsonResponse(serializer.data)

    return HttpResponseNotFound()


def next_game_pos(game) -> GamePos:
    room, round, question = game.room, game.round_num, game.question_num
    match room:
        case GameState.Room.LOBBY:
            return GamePos(GameState.Room.ROUND_START, round, question)
        case GameState.Room.ROUND_START:
            return GamePos(GameState.Room.QUIZ, round, question)
        case GameState.Room.QUIZ:
            if game.question_num >= len(game.cur_round) - 1:
                return GamePos(GameState.Room.SCOREBOARD, round, question)
            return GamePos(GameState.Room.SCOREBOARD, round, question + 1)
        case GameState.Room.SCOREBOARD:
            if game.round_num >= len(game.quiz) - 1:
                return GamePos(GameState.Room.GAME_END, round, question)
            return GamePos(GameState.Room.ROUND_START, round + 1, 0)
        case GameState.Room.GAME_END:
            print("Finished game")
            return GamePos(GameState.Room.GAME_END, round, question)
        case _:
            print("Invalid state transition")
            return None


def prev_game_pos(game) -> GamePos:
    room, round, question = game.room, game.round_num, game.question_num
    match room:
        case GameState.Room.LOBBY:
            print("Already at start of game")
            return GamePos(room, round, question)
        case GameState.Room.ROUND_START:
            if game.round_num == 0:
                return GamePos(GameState.Room.LOBBY, round, question)
            return GamePos(GameState.Room.SCOREBOARD, round - 1, len(game.prev_round) - 1)
        case GameState.Room.QUIZ:
            if game.question_num == 0:
                return GamePos(GameState.Room.ROUND_START, round, question)
            return GamePos(GameState.Room.QUIZ, round, question - 1)
        case GameState.Room.SCOREBOARD:
            return GamePos(GameState.Room.QUIZ, round, question)
        case GameState.Room.GAME_END:
            return GamePos(GameState.Room.SCOREBOARD, round, question)
        case _:
            print("Invalid state transition")
            return None
