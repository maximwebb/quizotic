from .common import get_cur_game_state
from ..models import GameState, Round, QuizRound, RoundQuestion, MultiChoiceQuestion, Choice

from django.shortcuts import render
from django.http import HttpResponse


def is_submitted(team_id, question_id):
    return False


def question_view(request):
    return mcq_view(request)


def mcq_view(request):
    gs = get_cur_game_state(request)
    round = QuizRound.objects.all()[gs.round_num].round

    questions = RoundQuestion.objects.all().filter(round=round)
    question = questions[gs.question_num].question
    choices = Choice.objects.all().filter(question=question.id)
    context = {"question": question, "choices": choices}

    return render(request, "quiz/mcq.html", context)


def submitted_view(request):
    return render(request, "quiz/submitted.html")
