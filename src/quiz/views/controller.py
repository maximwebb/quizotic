from .. import events
from ..models import *
from ..serializers import GameStateSerializer

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest, JsonResponse
from django.core import serializers

import json

"""TODO: Refactor this file into controller directory"""

# Game views


def game_select_view(request):
    context = {}
    games = GameState.objects.all().order_by("-created")

    context["games"] = games
    return render(request, "controller/index.html", context)


def game_view(request, game_id):
    if request.method == "GET":
        game = GameState.objects.values().get(pk=game_id)
        context = {"game": game}
        return render(request, "controller/game.html", context)


def game_state_view(request, game_id):
    if request.method == "GET":
        game = GameState.objects.get(pk=game_id)
        context = {"game": game}
        return render(request, "controller/game_state.html", context)


def game(request, game_id=None):
    if game_id is None:
        if request.method == "POST":
            game = GameState()
            game.save()
            serializer = GameStateSerializer(game)
            return JsonResponse(serializer.data)
        elif request.method == "GET":
            games = GameState.objects.all().order_by("-created")
            serializer = GameStateSerializer(games, many=True)
            return JsonResponse(serializer.data, safe=False)
        else:
            return None

    if request.method == "GET":
        game = GameState.objects.values().get(pk=game_id)
        serializer = GameStateSerializer(game)
        return JsonResponse(serializer.data)

    return None


def create_quiz_from_file(request):
    path = "quizzes/sample_quiz.json"
    with open(path) as f:
        data = json.load(f)

    rounds = []
    quiz = Quiz(name=data["name"])
    quiz.save()
    for r_i, r in enumerate(data["rounds"]):
        round = Round(name=r["name"])
        ord_round = OrderedRound(quiz=quiz, round=round, order=r_i)

        round.save()
        ord_round.save()

        for q_i, q in enumerate(r["questions"]):
            prompt = q["prompt"]

            if q["type"] == "mcq":
                question = MultiChoiceQuestion(prompt=prompt, round=round)
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

            ord_question = OrderedQuestion(round=round, question=question, order=q_i)
            ord_question.save()
            question.save()
            round.questions.add(question)

        round.save()
        ord_round.save()

        quiz.rounds.add(round)

    quiz.save()

    return HttpResponse()


def game_action(request, game_id: int, action: str):
    game = GameState.objects.all().get(pk=game_id)
    if request.method == "POST":
        if action == "next-question":
            game.question += 1
        elif action == "prev-question":
            game.question -= 1
        else:
            return HttpResponseNotFound()

        game.save()
        serializer = GameStateSerializer(game)
        return JsonResponse(serializer.data)

    return HttpResponseNotFound()


def game_room(request, game_id: int, room: str = None):
    game = GameState.objects.all().get(pk=game_id)
    print(room)
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
        events.push_room_update()
        return JsonResponse(serializer.data)

    return HttpResponseNotFound()
