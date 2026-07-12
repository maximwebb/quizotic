from django.shortcuts import render
from django.http import HttpResponse
from ..models import GameState, Round, MultiChoiceQuestion, Choice

def cur_question_view(request):
    game_state = GameState.objects.all().order_by("-created")[0]
    question = game_state.cur_round.cur_question
    context = { "question": question }

    return render(request, "quiz/mcq.html", context)

def setup(request):
    if request.method == "POST" or True:
        questions = ["What's the capital of Australia?", "What do you call an eight-sided shape?"]
        c_lists = [["Sydney", "Canberra", "Melbourne", "Perth"], ["Square", "Hexagon", "Heptagon", "Octagon"]]
        answers = [1, 3]
        choice_lists = []
        for c_list in c_lists:
            choice_list = []
            for c in c_list:
                choice = Choice(text=c)
                choice.save()
                choice_list.append(choice)
            choice_lists.append(choice_list)

        mcqs = []
        for q, cs, a in zip(questions, choice_lists, answers):
            mcq = MultiChoiceQuestion(question=q, answer=a)
            mcq.save()
            mcqs.append(mcq)

        r = Round(cur_question=mcqs[0])
        r.questions.set(mcqs)
        r.save()
    elif request.method == "XGET":
        r = Round.objects.all().order_by("-created")[0]
    context = { "question": r.cur_question }
        
    return render(request, "quiz/mcq.html", context)
