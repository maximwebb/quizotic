from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .lobby import lobby_view
from ..forms import CreateTeamForm
from ..models import Team
from .. import events

def create(request):
	if request.method == "POST":
		print(f"Received POST (team name: {request.POST.keys()}")
		context = {}
		team_name = request.POST["team_name"]
		team_leader = request.POST["team_leader"]
		request.session["team_name"] = team_name

		team = Team(team_name=team_name, team_leader=team_leader)
		team.save()

		events.push_teams_update()

		return HttpResponseRedirect(reverse("lobby"))

	form = CreateTeamForm()
	context = { "form": form }

	return render(request, "teams/create.html", context)


def list(request):
	teams = Team.objects.all()
	return render(request, "teams/list.html", { "teams": teams })
