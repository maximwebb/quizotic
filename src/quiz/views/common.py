from ..models import GameState, Team

from django.conf import settings

import os


def get_game_by_code(code):
    return GameState.objects.filter(code=code)[0]


def get_cur_team(request):
    name = request.session["team_name"]
    return Team.objects.filter(team_name=name)[0]


class FileStore:
    def store(file, name=""):
        print(os.listdir(settings.MEDIA_ROOT))
        return name

    def load(file):
        return ""
