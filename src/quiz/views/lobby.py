from django.shortcuts import render
from django.http import HttpResponse
from ..models import Team


def lobby_view(request):
    team_dict = {}

    teams = Team.objects.all()
    team_name = request.session["team_name"]
    cur_team = [t for t in teams if t.team_name == team_name][0]

    context = {}
    context["teams"] = teams
    context["cur_team"] = cur_team
    print(f"lobby ctx: {context}")

    return render(request, "lobby.html", context)
