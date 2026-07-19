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
class RoundQuestion(models.Model):
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
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class MultiChoiceQuestion(Question):
    pass


class Round(models.Model):
    name = models.CharField(max_length=128, blank=True)
    questions = models.ManyToManyField(
        Question, through=RoundQuestion, related_name="+")

    def __len__(self):
        return self.questions.count()

    def __str__(self):
        return self.name


class QuizRound(models.Model):
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
    rounds = models.ManyToManyField(Round, through=QuizRound, related_name="+")

    def __len__(self):
        return self.rounds.count()

    def __str__(self):
        return self.name


class Submission(models.Model):
    question = models.ForeignKey(RoundQuestion, on_delete=models.CASCADE)
    game = models.ForeignKey("GameState", on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    class Status(models.IntegerChoices):
        PENDING = 1, "pending"
        CORRECT = 2, "correct"
        INCORRECT = 3, "incorrect"

    status = models.IntegerField(choices=Status, default=Status.PENDING)
    points = models.IntegerField(default=0)

    @property
    def question_num(self):
        return self.question.order

    @property
    def round_num(self):
        return QuizRound.objects.get(round=self.question.round, quiz=self.game.quiz).order

    def __str__(self):
        return f"{self.team.team_name}|R{self.round_num}|Q{self.question_num}|{self.status}"


class GameState(models.Model):
    created = models.DateTimeField(default=datetime.now, blank=True)
    round_num = models.IntegerField(default=0)
    question_num = models.IntegerField(default=0)

    class Room(models.IntegerChoices):
        LOBBY = 1, "Lobby"
        QUIZ = 2, "Quiz"
        ROUND_END = 3, "Round End"
        GAME_END = 4, "Game End"

    room = models.IntegerField(choices=Room, default=Room.LOBBY)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    @property
    def cur_round(self):
        return QuizRound.objects.get(quiz=self.quiz, order=self.round_num).round

    @property
    def cur_round_question(self):
        return RoundQuestion.objects.get(round=self.cur_round, order=self.question_num)

    @property
    def cur_question(self):
        return self.cur_round_question.question

    def __str__(self):
        return f"Room: {self.room} Round: {self.round_num} Question: {self.question_num}"


class Image(models.Model):
    path = models.CharField(max_length=256)
    alt = models.CharField(max_length=64)

    def __str__(self):
        return self.alt
