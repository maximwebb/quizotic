from django.db import models

class Team(models.Model):
	team_name = models.CharField(max_length=128, blank=True)
	team_leader = models.CharField(max_length=128, blank=True)	

	def __str__(self):
		return f"{self.team_name}|{self.team_leader}"
