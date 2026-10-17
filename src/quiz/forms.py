from .models import GameState, Team

from django import forms
from django.utils.html import format_html
from django.utils.safestring import mark_safe


class CreateGameForm(forms.Form):
    new_quiz = forms.FileField()


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


class TextboxForm(forms.Form):
    text = forms.CharField(label=False, max_length="256", widget=forms.Textarea(attrs={
        "class": "textbox std-input",
        "autocomplete": "off",
        "placeholder": "Max length 256",
        "cols": "20",
        "rows": "4"
    }))


class VoteWidget(forms.RadioSelect):
    option_template_name = "forms/vote_choice.html"


class VoteForm(forms.Form):
    choices = forms.ModelChoiceField

    def __init__(self, teams, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["choices"] = forms.ModelChoiceField(
            queryset=teams,
            empty_label=None,
            widget=VoteWidget(attrs={"class": "multi-choice"}),
            label=False,
        )
