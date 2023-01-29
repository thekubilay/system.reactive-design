from django.test import TestCase
from tasks.models import Task

print(Task.objects.filter(task_name__icontains="HTMLメール新規作成・納品"))
