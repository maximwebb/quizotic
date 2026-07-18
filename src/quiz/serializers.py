from .models import GameState

from rest_framework import serializers


class GameStateSerializer(serializers.ModelSerializer):
	class Meta:
		model = GameState
		fields = "__all__"
