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

	class Room(models.IntegerChoices):
		LOBBY = 1, "Lobby"
		QUIZ = 2, "Quiz"
		ROUND_END = 3, "Round End"
		GAME_END = 4, "Game End"

	room = models.IntegerField(choices=Room, db_default=Room.LOBBY)

	def __str__(self):
		return f"Room: {self.room} Round: {self.quiz_round} Question: {self.question}"

