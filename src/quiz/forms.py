from django import forms


class CreateTeamForm(forms.Form):
    team_name = forms.CharField(label="Team Name", max_length="128")
    team_leader = forms.CharField(label="Team Leader", max_length="128")
