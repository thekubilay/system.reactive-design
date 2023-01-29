from rest_framework import viewsets
from rest_framework.response import Response
from teams.models import Team
from teams.apis.serializers import TeamsSerializer


class TeamsViewSet(viewsets.ViewSet):
  def list(self, request, *args, **kwargs):
    queryset = Team.objects.all()
    serializer = TeamsSerializer(queryset, many=True)
    return Response(serializer.data)
