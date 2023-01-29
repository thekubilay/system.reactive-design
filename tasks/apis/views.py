from rest_framework import viewsets
from rest_framework.response import Response
from django.db.models import Q
from teams.models import TeamFilter
from tasks.models import Task
from tasks.apis.serializers import TasksSerializer


class TasksViewSet(viewsets.ViewSet):
  def list(self, request, *args, **kwargs):
    pass