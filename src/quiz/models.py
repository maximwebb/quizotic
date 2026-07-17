from django.db import models
from datetime import datetime

class Team(models.Model):
	team_name = models.CharField(max_length=128, blank=True)
	team_leader = models.CharField(max_length=128, blank=True)	

	def __str__(self):
		return f"{self.team_name}|{self.team_leader}"


# Base class for question
class Question(models.Model):
	prompt = models.CharField(max_length=256)
	
	def __str__(self):
		return self.prompt


# Question with additional ordering info specific to the round
class OrderedQuestion(models.Model):
	round = models.ForeignKey("Round", on_delete=models.CASCADE)
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	order = models.PositiveIntegerField()

	class Meta:
		ordering = ["order"]
		# DB constraint - ensures these combinations of columns are unique
		unique_together = [("round", "order")]
		unique_together = [("round", "question")]


class Choice(models.Model):
	text = models.CharField(max_length=128, blank=True)
	question = models.ForeignKey("MultiChoiceQuestion", on_delete=models.CASCADE)
	is_correct = models.BooleanField(db_default=False)

	def __str__(self):
		return self.text


class MultiChoiceQuestion(Question):
	round = models.ForeignKey("Round", on_delete=models.CASCADE)


class Round(models.Model):
	name = models.CharField(max_length=128, blank=True)
	questions = models.ManyToManyField(Question, through=OrderedQuestion, related_name="+")

	def __str__(self):
		return self.name


class OrderedRound(models.Model):
	quiz = models.ForeignKey("Quiz", on_delete=models.CASCADE)
	round = models.ForeignKey(Round, on_delete=models.CASCADE)
	order = models.PositiveIntegerField()

	class Meta:
		ordering = ["order"]
		unique_together = [("quiz", "order")]
		unique_together = [("quiz", "round")]

	def __str__(self):
		return f"Round {self.order}"


class Quiz(models.Model):
	name = models.CharField(max_length=128, blank=True)
	rounds = models.ManyToManyField(Round, through=OrderedRound, related_name="+")

	def __str__(self):
		return self.name


class GameState(models.Model):
	created = models.DateTimeField(default=datetime.now, blank=True)
	round = models.IntegerField(db_default=1)
	question = models.IntegerField(db_default=1)

	class Room(models.IntegerChoices):
		LOBBY = 1, "Lobby"
		QUIZ = 2, "Quiz"
		ROUND_END = 3, "Round End"
		GAME_END = 4, "Game End"

	room = models.IntegerField(choices=Room, db_default=Room.LOBBY)

	def __str__(self):
		return f"Room: {self.room} Round: {self.round} Question: {self.question}"
