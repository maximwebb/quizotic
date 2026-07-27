from ..models import GameState, Team

import tempfile


def get_game_by_code(code):
    return GameState.objects.filter(code=code)[0]


def get_cur_team(request):
    name = request.session["team_name"]
    return Team.objects.filter(team_name=name)[0]


class FileStore:
	def store(file, team_name) -> str:
		with tempfile.NamedTemporaryFile(delete=False) as f:
			f.write(file.read())
			return f.name
	
