from ..common import get_game_by_code
from ...models import *

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, HttpResponseBadRequest, JsonResponse
from django.urls import reverse


def index(request, game_code: str):
    if request.method == "POST":
        submission_id = request.POST["submission_id"]
        is_correct = parse_bool(request.POST["is_correct"])
        if is_correct is None:
            print(f"Error parsing `is_correct`: {request.POST['is_correct']}")
            return HttpResponseBadRequest()
        submission = Submission.objects.get(id=submission_id)
        submission.status = Submission.Status.CORRECT if is_correct else Submission.Status.INCORRECT
        submission.save()

        return HttpResponse()

    elif request.method == "GET":
        game = get_game_by_code(game_code)
        unmarked = Submission.objects.filter(status=Submission.Status.PENDING, game=game.id)
        unmarked_text = TextSubmission.objects.filter(submission__in=unmarked).select_related('submission')
        context = {"unmarked": unmarked, "unmarked_text": unmarked_text, "game": game}
        return render(request, "controller/marking.html", context)
