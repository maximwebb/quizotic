from ..forms import JoinGameForm

from ..models import GameState

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


def home_view(request):
    if request.method == "POST":
        game_code = request.POST.get("game_code")

        if game_code is None or not GameState.objects.filter(code=game_code).exists():
            return HttpResponseBadRequest()

        return HttpResponseRedirect(reverse("create_team", args=(game_code,)))

    form = JoinGameForm()
    context = {"form": form}
    return render(request, "index.html", context)


def canvas_view(request):
    return render(request, "include/canvas.html")
