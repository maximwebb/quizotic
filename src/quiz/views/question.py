from .common import get_cur_game_state, get_cur_team
from ..models import GameState, Round, QuizRound, RoundQuestion, MultiChoiceQuestion, Choice, Submission
from ..forms import MCQForm, CreateTeamForm

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound


def is_submitted(team, question):
    return Submission.objects.filter(team=team, question=question).exists()


def question_view(request):
    gs = get_cur_game_state(request)
    team = get_cur_team(request)

    if is_submitted(team, gs.cur_round_question):
        return submitted_view(request)

    return mcq_view(request)


def mcq_view(request):
    gs = get_cur_game_state(request)
    team = get_cur_team(request)

    if request.method == "POST":
        ans = request.POST["choices"]
        choice = Choice.objects.get(pk=ans)
        print(choice)
        status = Submission.Status.CORRECT if choice.is_correct else Submission.Status.INCORRECT

        round_question = gs.cur_round_question
        submission = Submission(question=round_question, game=gs, team=team, status=status)
        submission.save()
        return redirect(request.path)
    elif request.method == "GET":
        question = gs.cur_question
        choices = Choice.objects.all().filter(question=question.id)
        form = MCQForm(choices)
        context = {"question": question, "form": form}

        return render(request, "quiz/mcq.html", context)
    else:
        return HttpResponseNotFound()


def submitted_view(request):
    return render(request, "quiz/submitted.html")
