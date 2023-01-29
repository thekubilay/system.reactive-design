import time
import mojimoji

from django.db.models import Q
from teams.models import Team, TeamFilter
from projects.models import Project
from tasks.models import Task
from commons.utils import send_mail, asana_api_connector, asana_task_deleted, asana_tasks

text = "！＂＃＄％＆＇（）＊＋，－．／０１２３４５６７８９：；＜＝＞？＠ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ［＼］＾＿｀>？＠ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ｛｜｝～"


def zenToHan(text):
  return text.translate(str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)}))


class AsanaApiCrawler:
  def __init__(self):
    self.projects = []

  def get_projects(self):
    teams = Team.objects.filter(tid="1202920776487810")
    for team in teams:

      url1 = f"https://app.asana.com/api/1.0/projects?archived=false&team={team.tid}"
      url2 = f"https://app.asana.com/api/1.0/projects?archived=true&team={team.tid}"

      # live projects
      self.projects = asana_api_connector(url1)
      for project in self.projects:
        name = zenToHan(project["name"]).split(":")[0]
        defaults = {"name": name}
        Project.objects.update_or_create(pid=int(project["gid"]), team=team, defaults=defaults)

      # archived projects
      self.projects.clear()
      self.projects = asana_api_connector(url2)
      for project in self.projects:
        name = zenToHan(project["name"]).split(":")[0]
        defaults = {"name": name, "archived": True}
        Project.objects.update_or_create(pid=project["gid"], team=team, defaults=defaults)

  def get_tasks(self):
    teams = Team.objects.all()
    for team in teams:
      filters = TeamFilter.objects.filter(team__tid=team.tid)
      keywords = []
      for ft in filters:
        keywords.append(ft.keywords)

      if len(keywords):
        string = " ".join(keywords)
        projects = None
        for keyword in keywords:
          qs = ((Q(team__tid=team.tid) & Q(archived=False)) | (Q(name=string) |
                                                               Q(name__in=keyword) |
                                                               Q(name__icontains=keyword)))
          projects = Project.objects.filter(qs)
      else:
        projects = Project.objects.filter(team=team, archived=False)

      if projects:
        for project in projects:
          print(project.pid, project.name)
          url = "https://app.asana.com/api/1.0/projects/" + str(
            project.pid) + "/tasks?opt_pretty&opt_expand=(this%7Csubtasks%2B)"
          # db_tasks = Task.objects.filter(project=project)
          tasks = asana_api_connector(url)
          errors = asana_tasks(project, tasks)
          # asana_task_deleted(db_tasks, tasks)

          # if errors:
          # print(errors)
          # send_mail("Reactive システムエラー", ["kubilay.turgut@reactive-design.com"], "asana_error_email", errors)

          time.sleep(1)
