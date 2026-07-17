from django.shortcuts import render
from django.http import HttpResponse
from ..models import GameState, Round, OrderedQuestion, MultiChoiceQuestion, Choice

def mcq_view(request):
    rnd = Round.objects.all()[0]
    questions = OrderedQuestion.objects.all().filter(round=rnd.id)
    question = questions[0].question
    choices = Choice.objects.all().filter(question=question.id)
    context = { "question": question, "choices": choices }

    return render(request, "quiz/mcq.html", context)

