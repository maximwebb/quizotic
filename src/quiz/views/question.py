from django.shortcuts import render
from django.http import HttpResponse
from ..models import GameState, Round, OrderedRound, OrderedQuestion, MultiChoiceQuestion, Choice

def get_game_state():
	return GameState.objects.first()

def mcq_view(request):
	gs = get_game_state()
	round = OrderedRound.objects.all()[gs.round].round

	questions = OrderedQuestion.objects.all().filter(round=round)
	question = questions[gs.question].question
	choices = Choice.objects.all().filter(question=question.id)
	context = { "question": question, "choices": choices }

	return render(request, "quiz/mcq.html", context)

