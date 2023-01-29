from rest_framework import serializers
from settings.apis.serializers import SettingsSerializer
from teams.models import Team


class TeamsSerializer(serializers.ModelSerializer):
  setting = SettingsSerializer()

  class Meta:
    model = Team
    fields = "__all__"
