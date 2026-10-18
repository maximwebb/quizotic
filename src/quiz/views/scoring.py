from .common import get_game_by_code, get_cur_question_by_code, get_cur_team
from ..models import *
from ..forms import MCQForm, TextboxForm, VoteForm

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound


def scoreboard_view(request, game_code: str):
    game = get_game_by_code(game_code)

    teams = Team.objects.all().filter(game=game)
    cur_round = game.cur_round

    data = [{"team": team, "round_score": get_round_score(team, cur_round, game), "total_score": get_total_score(team, game)} for team in teams]

    context = {"game": game, "data": data}
    return render(request, "scoreboard.html", context)


def get_total_score(team, game) -> int:
    res = 0
    for round_num in range(game.round_num + 1):
        # Can we make this a class method?
        round = QuizRound.objects.get(quiz=game.quiz, order=round_num).round
        res += get_round_score(team, round, game)

    return res


def get_round_score(team, round, game) -> int:
    res = 0

    for question in round.questions.all():
        round_question = RoundQuestion.objects.get(round=round, question=question)

        try:
            sub = Submission.objects.get(question=round_question, game=game, team=team)
        except BaseException:
            print(f"No submission found for question: {question}, team: {team} skipping...")
            continue
        match question.marking_type:
            # Get all auto/host-marked scores:
            case Question.Marking.AUTO | Question.Marking.HOST:
                res += question.points if sub.status == Submission.Status.CORRECT else 0
            # Get all user-voted scores:
            case Question.Marking.VOTE:
                try:
                    votes = Submission.objects.all().filter(question=round_question)
                    vote_count = VoteSubmission.objects.all().filter(submission__in=votes, team_choice=team).count()
                except BaseException:
                    print(f"No vote found for question: {question}, team: {team} skipping...")
                    continue
                if VoteSubmission.objects.all().filter(submission=sub, team_choice=team).count() > 0:
                    print(f"Team {team} voted for themselves - for shame!")
                    res -= 1
                else:
                    res += vote_count * question.points
            case _:
                raise f"Scoring not supported, {question}"

    return res
