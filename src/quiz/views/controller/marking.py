from ..common import get_game_by_code
from ..util import parse_bool
from ...models import *

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, HttpResponseBadRequest, JsonResponse
from django.urls import reverse


def index(request, game_code: str):
    if request.method == "POST":
        submission_id = request.POST["submission_id"]
        is_correct = request.POST["is_correct"].lower()
        match is_correct:
            case "true":
                status = Submission.Status.CORRECT
            case "false":
                status = Submission.Status.INCORRECT
            case "half":
                status = Submission.Status.HALF
            case _:
                print(f"Error parsing `is_correct`: {request.POST['is_correct']}")
                return HttpResponseBadRequest()
        submission = Submission.objects.get(id=submission_id)
        submission.status = status
        submission.save()

        return HttpResponse()

    elif request.method == "GET":
        game = get_game_by_code(game_code)
        unmarked = Submission.objects.filter(status=Submission.Status.PENDING, game=game.id)
        unmarked_text = TextSubmission.objects.filter(submission__in=unmarked).select_related('submission')
        submissions = get_round_submissions(game)
        context = {"unmarked": unmarked, "unmarked_text": unmarked_text, "game": game, "questions": submissions}
        return render(request, "controller/marking.html", context)


def get_round_submissions(game):
    res = []
    for q_i in range(game.question_num + 1):
        q = RoundQuestion.objects.get(round=game.cur_round, order=q_i)
        subs = []
        for s in Submission.objects.filter(question=q.id):
            text = "n/a"
            if TextSubmission.objects.filter(submission=s.id):
                text = TextSubmission.objects.get(submission=s.id).text

            sub = {"team_name": s.team.team_name, "text": text, "status": s.get_status_display()}
            subs.append(sub)
        q_dict = {"prompt": q.question.prompt, "subs": subs}
        print(q)
        res.append(q_dict)
    return reversed(res)
