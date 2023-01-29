import mojimoji
import requests
import datetime
import re

from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from tasks.models import Task


def zenToHan(text):
  return text.translate(str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)}))


def send_mail(subject, emails, path, errors):
  message = render_to_string(f"emails/{path}.html", {
    "errors": errors
  })
  send_email = EmailMessage(subject, message, to=emails)
  send_email.send()


def asana_api_connector(url):
  response = requests.get(url, headers={"Authorization": "Bearer 0/84c8f71787ba23de08c82291a01ec4c9"}).json()
  return response["data"]


def asana_task_deleted(db_tasks, asana_tasks):
  asana_ids = []
  for task in asana_tasks:
    asana_ids.append(task["gid"])

  db_ids = []
  for task in db_tasks:
    db_ids.append(str(task.task_id))

  non_match = []
  for i in db_ids:
    if i not in asana_ids:
      non_match.append(i)

  for tid in non_match:
    tasks = Task.objects.filter(task_id=tid)
    for task in tasks:
      task.delete()


def asana_task_custom_fields(task, reformat):
  for field in task["custom_fields"]:
    if field["name"] == "ステータス":
      if "display_value" in field and field["display_value"] is not None and zenToHan(field["display_value"]) == "本番公開完了":
        reformat["task_over"] = True
      else:
        reformat["task_over"] = False

    if field["name"] == "数量":
      if "number_value" in field and field["number_value"] is not None:
        reformat["task_count"] = zenToHan(str(field["number_value"]))
      elif "text_value" in field and field["text_value"] is not None:
        reformat["task_count"] = zenToHan(field["text_value"])

    if field["name"] == "単位" and field["text_value"] is not None:
      reformat["task_kind"] = field["text_value"]

    if field["name"] == "単価":
      if "number_value" in field and field["number_value"] is not None:
        reformat["task_price"] = zenToHan(str(field["number_value"]))
      elif "text_value" in field and field["text_value"] is not None:
        reformat["task_price"] = field["text_value"]

    else:
      pass

  return reformat


def asana_task_invoice_date(task, reformat):
  now = datetime.datetime.now()

  for field in task["memberships"]:
    if str(now.year) in field["section"]["name"] or "2022" in field["section"]["name"]:
      reformat["task_invoice_date"] = re.findall(r'\d+', zenToHan(field["section"]["name"]))

  return reformat


def asana_task_calculate_total_price(reformat):
  if reformat["task_price"] and reformat["task_count"]:
    try:
      reformat["task_total_price"] = int(reformat["task_price"]) * int(reformat["task_count"])
    except:
      pass
  return reformat


def asana_tasks(project, task_list):
  errors = []
  for i, task in enumerate(task_list):
    before_format = {
      "permalink": f"https://app.asana.com/0/{project.pid}/{task['gid']}",
      "task_status": task["completed"],
      "task_name": task["name"],
      "task_count": None,
      "task_kind": None,
      "task_price": None,
      "task_total_price": None,
      "task_over": False,
      "task_invoice_date": None,
      "task_due_date": task["due_on"],
      "task_modified_at": task["modified_at"],
      "task_completed_at": task["completed_at"],
      "task_created_at": task["created_at"],
    }

    reformat1 = asana_task_custom_fields(task, before_format)
    reformat2 = asana_task_invoice_date(task, reformat1)
    reformat3 = asana_task_calculate_total_price(reformat2)
    invoice_date = reformat3["task_invoice_date"]

    # print(task["gid"])
    # print(invoice_date, len(invoice_date), project.name)

    if invoice_date:
      if int(task["gid"]) == 1201436024649103:
        pass
        # print(reformat3)

      if len(invoice_date) == 3:
        reformat3["task_invoice_date"] = "-".join(invoice_date)
      elif len(invoice_date) > 3:
        reformat3["task_invoice_date"] = "-".join(invoice_date[:3])
      else:
        katachi = "-".join(invoice_date)
        permalink = reformat3["permalink"]
        errors.append("日付形エラー: 「" + katachi + "」<br> タスクリンク: " + permalink)
        reformat3["task_invoice_date"] = None

      Task.objects.update_or_create(task_id=task["gid"], project_id=project.id, defaults=reformat3)

  return errors
