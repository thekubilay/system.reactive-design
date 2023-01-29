import datetime

from rest_framework import viewsets
from rest_framework.response import Response
from django.db.models import Q, Prefetch
from teams.models import TeamFilter
from projects.models import Project
from tasks.models import Task
from projects.apis.serializers import ProjectsSerializer, ProjectsReordersSerializer


class ProjectsViewSet(viewsets.ViewSet):
  def list(self, request, *args, **kwargs):
    startDate = self.request.query_params.get("start_date")
    endDate = self.request.query_params.get("end_date")
    teamId = self.request.query_params.get("tid")
    filters = TeamFilter.objects.filter(team__tid=teamId)
    keywords = []
    for ft in filters:
      keywords.append(ft.keywords)

    string = " ".join(keywords)
    queryset = Project.objects.filter(team_id=int(teamId))

    if len(keywords):
      for keyword in keywords:
        qs = (Q(team__tid=int(teamId)) & Q(archived=False) | (Q(name=string) |
                                                              Q(name__in=keyword) |
                                                              Q(name__icontains=keyword)))
        queryset = Project.objects.prefetch_related(
          Prefetch('tasks', queryset=Task.objects.filter(task_status=True, task_over=True,
                                                         task_invoice_date__range=[startDate, endDate]))).filter(qs)
    else:
      queryset = Project.objects.prefetch_related(
        Prefetch('tasks', queryset=Task.objects.filter(task_status=True, task_over=True,
                                                       task_invoice_date__range=[startDate, endDate]))).filter(team__tid=int(teamId))

    serializer = ProjectsSerializer(queryset, many=True)
    for project in serializer.data:
      project["styles"] = {
        "display": False,
        "headerTitleFontSize": 15,
        "headerContentTextFontSize": 11,
        "headerBrandTextSize": 13,
        "bodyContentFontSize": 10,
      }
      project["tasks_total"] = 0
      project["tax"] = 0
      for task in project["tasks"]:
        if task["task_count"] is not None and task["task_count"].isdigit() and (
          task["task_price"] is not None and task["task_price"].isdigit()):
          project["tasks_total"] += int(task["task_total_price"])

      project["tax"] = (10 * project["tasks_total"]) / 100
      project["tax"] = str(project["tax"]).split(".")[0]

    projects_with_tasks = filter(lambda x: len(x["tasks"]), serializer.data)

    return Response(projects_with_tasks)

  def partial_update(self, request, *args, **kwargs):
    instance = Project.objects.get(pk=kwargs.get('pk'))
    serializer = ProjectsSerializer(instance, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


class ProjectsReordersViewSet(viewsets.ViewSet):
  serializer_class = ProjectsReordersSerializer

  def create(self, request):
    if "reordered" in request.data:
      items = request.data["reordered"]
      for i, item in enumerate(items):
        project = Project.objects.get(id=item["id"])
        project.oid = i + 1
        project.save()

    return Response(status=200)
