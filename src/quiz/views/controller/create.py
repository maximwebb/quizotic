from ...forms import CreateGameForm
from ...models import *

from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, HttpResponseBadRequest, JsonResponse
from django.urls import reverse

import random
import json
import string


def index(request):
    games = GameState.objects.all().order_by("-created")
    context = {"games": games}
    return render(request, "controller/index.html", context)


def create(request):
    if request.method == "POST":
        files = request.FILES
        print(request.POST)
        if len(files) == 1:
            file = next(files.values())
            quiz = create_quiz_from_json(file.read())
            quiz.save()
        elif request.POST["quiz_id"] is not None:
            quiz = Quiz.objects.get(id=request.POST["quiz_id"])
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


def create_quiz_from_json(raw):
    try:
        data = json.loads(raw)
    except Exception as e:
        print(f"error: {e}")

    rounds = []
    quiz = Quiz(name=data["name"])
    quiz.save()
    for r_num, r in enumerate(data["rounds"]):
        round = Round(name=r["name"])
        round.save()

        ord_round = QuizRound(quiz=quiz, round=round, order=r_num)
        ord_round.save()

        vote_questions = []

        q_num = 0
        for q in r["questions"]:
            prompt = q["prompt"]
            marking = Question.Marking.from_str(q["marking"]) if "marking" in q else Question.Marking.NONE
            points = q["points"] if "points" in q else 0
            image = q["image"] if "image" in q else None

            match q["type"]:
                case "mcq":
                    question = MultiChoiceQuestion(prompt=prompt, marking_type=Question.Marking.AUTO, points=points, image=image)
                    question.save()

                    ans = q["answer"]
                    exists_correct = False
                    for c in q["choices"]:
                        is_correct = c == ans
                        exists_correct |= is_correct
                        choice = Choice(text=c, question=question, is_correct=is_correct)
                        choice.save()
                    if not exists_correct:
                        print(f"[R{r_num}|Q{q_num}] MCQ answer \"{ans}\" not included in choices: {','.join(q['choices'])}")
                        return HttpResponseBadRequest()
                case "textbox":
                    question = TextboxQuestion(
                        prompt=prompt,
                        marking_type=marking,
                        points=0 if marking == Question.Marking.VOTE else points,
                        image=image)
                    question.save()

                case _:
                    print(f"[R{r_num}|Q{q_num}] got bad question type: {q['type']}")
                    return HttpResponseBadRequest()

            ord_question = RoundQuestion(round=round, question=question, order=q_num)
            ord_question.save()
            question.save()

            if marking == Question.Marking.VOTE:
                vote = VoteQuestion(prompt="", parent=ord_question, marking_type=Question.Marking.NONE, points=points)
                vote_questions.append(vote)
                vote.save()

            round.questions.add(question)
            q_num += 1

        for i, vote in enumerate(vote_questions):
            ord_vote = RoundQuestion(round=round, question=vote, order=q_num)
            ord_vote.save()
            round.questions.add(vote)
            q_num += 1

        round.save()
        ord_round.save()

        quiz.rounds.add(round)

    quiz.save()

    return quiz
