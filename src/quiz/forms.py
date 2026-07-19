from django import forms


class CreateTeamForm(forms.Form):
    team_name = forms.CharField(label="Team Name", max_length="128")
    team_leader = forms.CharField(label="Team Leader", max_length="128")


class MCQForm(forms.Form):
    choices = forms.MultipleChoiceField(choices=[])

    def __init__(self, choices, *args, **kwargs):
        super(MCQForm, self).__init__(*args, **kwargs)
        self.fields["choices"] = forms.MultipleChoiceField(choices=[(c.id, c.text) for c in choices])
