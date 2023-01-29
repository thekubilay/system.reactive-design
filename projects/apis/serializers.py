from rest_framework import serializers
from projects.models import Project
from tasks.apis.serializers import TasksSerializer


class ProjectsSerializer(serializers.ModelSerializer):
  tasks = TasksSerializer(many=True, read_only=True)

  class Meta:
    model = Project
    fields = ("id", "archived", "gid", "company_name", "name", "tasks", "oid", "pid", "team")
    depth = 1


class ProjectsReordersSerializer(serializers.ModelSerializer):
  class Meta:
    model = Project
    fields = "__all__"
