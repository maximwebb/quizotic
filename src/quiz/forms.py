from .models import GameState

from django import forms


class JoinGameForm(forms.Form):
    game_code = forms.CharField(label="Game Code", min_length="6", max_length="6", widget=forms.TextInput(attrs={
        "class": "game-code"
    }))


class CreateTeamForm(forms.Form):
    team_name = forms.CharField(label=False, max_length="128", widget=forms.TextInput(attrs={
        "class": "create-team-input std-input cartoon-indent",
        "autocomplete": "off",
        "placeholder": "TEAM NAME"
    }))
    team_leader = forms.CharField(label=False, max_length="128", widget=forms.TextInput(attrs={
        "class": "create-team-input std-input cartoon-indent",
        "autocomplete": "off",
        "placeholder": "TEAM LEADER"
    }))


class ProfilePicForm(forms.Form):
    image = forms.FileField()


class MCQForm(forms.Form):
    choices = forms.ChoiceField(
        label=False,
        widget=forms.RadioSelect(attrs={"class": "multi-choice"})
    )

    def __init__(self, choices, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["choices"].choices = [
            (c.id, c.text) for c in choices
        ]
