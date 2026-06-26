from django.db import models
from datetime import datetime

class Team(models.Model):
	team_name = models.CharField(max_length=128, blank=True)
	team_leader = models.CharField(max_length=128, blank=True)	

	def __str__(self):
		return f"{self.team_name}|{self.team_leader}"


class GameState(models.Model):
	created = models.DateTimeField(default=datetime.now, blank=True)
	quiz_round = models.IntegerField(db_default=1)
	question = models.IntegerField(db_default=1)

	class Stage(models.IntegerChoices):
		LOBBY = 1
		GAME = 2
		ROUND_END = 3
		GAME_END = 4

		def __str__(self):
			if self == Stage.LOBBY:
				return "Lobby"
			elif self == Stage.GAME:
				return "Round"
			elif self == Stage.ROUND_END:
				return "Round End"
			else:
				return "Game End"
	
	stage = models.IntegerField(choices=Stage, db_default=Stage.LOBBY)

	def __str__(self):
		return f"Stage: {self.stage} Round: {self.quiz_round} Question: {self.question}"

