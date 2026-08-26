from .models import GameState

from django import forms


class JoinGameForm(forms.Form):
    # TODO: Use an uppercase class to avoid inlining CSS here
    game_code = forms.CharField(label="Game Code", min_length="6", max_length="6", widget=forms.TextInput(attrs={
        "class": "game-code"
    }))


class CreateTeamForm(forms.Form):
    team_name = forms.CharField(label="Team Name", max_length="128")
    team_leader = forms.CharField(label="Team Leader", max_length="128")


class ProfilePicForm(forms.Form):
    image = forms.FileField()


class MCQForm(forms.Form):
    choices = forms.MultipleChoiceField(choices=[])

    def __init__(self, choices, *args, **kwargs):
        super(MCQForm, self).__init__(*args, **kwargs)
        self.fields["choices"] = forms.MultipleChoiceField(choices=[(c.id, c.text) for c in choices])
