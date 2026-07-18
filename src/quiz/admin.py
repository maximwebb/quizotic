from django.contrib import admin

from .models import *

admin.site.register(GameState)
admin.site.register(Team)

# Display many-to-many relationships in admin dashboard


class QuizToRound(admin.TabularInline):
    model = Quiz.rounds.through
    ordering = ("order",)


class RoundToQuestion(admin.TabularInline):
    model = Round.questions.through
    ordering = ("order",)


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    inlines = [QuizToRound]
    exclude = ("rounds",)


@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
    # Include QuizToRound to view list of Quizzes this round belongs to
    inlines = [RoundToQuestion]
    exclude = ("questions",)


# Display foreign-key relationships in admin dashboard

class ChoiceInline(admin.TabularInline):
    model = Choice


@admin.register(MultiChoiceQuestion)
class MCQAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
