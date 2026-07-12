from django.contrib import admin

from .models import GameState, Team, Question, OrderedQuestion, Choice, MultiChoiceQuestion, Round

admin.site.register(GameState)
admin.site.register(Team)
admin.site.register(Question)
admin.site.register(OrderedQuestion)
admin.site.register(Choice)
admin.site.register(MultiChoiceQuestion)
admin.site.register(Round)
