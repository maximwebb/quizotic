from .. import events
from ..forms import CreateGameForm
from ..models import *
from ..serializers import GameStateSerializer
from ..views.common import get_game_by_code

from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, HttpResponseBadRequest, JsonResponse
from django.urls import reverse

import json
import random
import string

"""TODO: Refactor this file into controller directory"""

# Game views


def game_select_view(request):
    context = {}
    games = GameState.objects.all().order_by("-created")
    print(games)

    context["games"] = games
    return render(request, "controller/index.html", context)


def create_game(request):
    if request.method == "POST":
        files = request.FILES
        if len(files) == 1:
            file = next(files.values())
            quiz = create_quiz_from_json(file.read())
            quiz.save()
        elif request.POST["quiz_id"] is not None:
            quiz = quiz.objects.get(id=quiz_id)
        else:
            return HttpResponseNotFound()

        game_code = ''.join(random.choices(string.ascii_uppercase, k=6))
        game = GameState(quiz=quiz, code=game_code)
        game.save()

        return HttpResponseRedirect(reverse("controller_game", args=(game_code,)))

    elif request.method == "GET":
        quiz_list = Quiz.objects.all().order_by("-created")[:6]
        form = CreateGameForm()
        context = {"form": form, "quiz_list": quiz_list}

        return render(request, "controller/create.html", context)

    return HttpResponseNotFound()


def game_view(request, game_code: str):
    if request.method == "GET":
        game = get_game_by_code(game_code)
        context = {"game": game}
        return render(request, "controller/game.html", context)


def game_state_view(request, game_code: str):
    if request.method == "GET":
        game = get_game_by_code(game_code)
        context = {"game": game}
        return render(request, "controller/game_state.html", context)


def game(request, game_code=None):
    if request.method != "GET":
        return HttpResponseNotFound()

    # List all games if no game code specified
    if game_code is None:
        games = GameState.objects.all().order_by("-created")
        serializer = GameStateSerializer(games, many=True)
        return JsonResponse(serializer.data, safe=False)

    game = get_game_by_code(game_code)
    serializer = GameStateSerializer(game)
    return JsonResponse(serializer.data)


def create_quiz_from_json(raw):
    try:
        data = json.loads(raw)
    except Exception as e:
        print(f"error: {e}")

    rounds = []
    quiz = Quiz(name=data["name"])
    quiz.save()
    for r_i, r in enumerate(data["rounds"]):
        round = Round(name=r["name"])
        round.save()

        ord_round = QuizRound(quiz=quiz, round=round, order=r_i)
        ord_round.save()

        for q_i, q in enumerate(r["questions"]):
            prompt = q["prompt"]

            if q["type"] == "mcq":
                question = MultiChoiceQuestion(prompt=prompt)
                question.save()

                ans = q["answer"]
                exists_correct = False
                for c in q["choices"]:
                    is_correct = c == ans
                    exists_correct |= is_correct
                    choice = Choice(text=c, question=question, is_correct=is_correct)
                    choice.save()
                if not exists_correct:
                    print(f"[R{r_i}|Q{q_i}] MCQ answer \"{ans}\" not included in choices: {','.join(q['choices'])}")
                    return HttpResponseBadRequest()
            else:
                print(f"[R{r_i}|Q{q_i}] got bad question type: {q['type']}")
                return HttpResponseBadRequest()

            ord_question = RoundQuestion(round=round, question=question, order=q_i)
            ord_question.save()
            question.save()
            round.questions.add(question)

        round.save()
        ord_round.save()

        quiz.rounds.add(round)

    quiz.save()

    return quiz


def game_action(request, game_code: str, action: str):
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


def game_room(request, game_code: str, room: str = None):
    game = get_game_by_code(game_code)
    prev_room = GameState.Room(game.room)
    if request.method == "POST":
        print(f"Changing {prev_room.label.lower()} --> {room}")
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
