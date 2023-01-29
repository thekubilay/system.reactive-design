import random

from django.db import models
from projects.models import Project

class Task(models.Model):
  project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks', blank=True, null=True)
  permalink = models.URLField(null=True, blank=False, max_length=255)
  task_id = models.BigIntegerField(null=True, blank=False)
  task_status = models.BooleanField(default=False, null=False)
  task_name = models.CharField(max_length=255, blank=True, null=True)
  task_count = models.CharField(max_length=255, blank=True, null=True)
  task_kind = models.CharField(max_length=255, blank=True, null=True)
  task_price = models.CharField(max_length=255, blank=True, null=True)
  task_total_price = models.IntegerField(blank=True, null=True)
  task_over = models.BooleanField(default=False)
  task_invoice_date = models.DateField(null=True, blank=False)
  task_due_date = models.CharField(max_length=255, blank=True, null=True)
  task_modified_at = models.CharField(max_length=255, blank=True, null=True)
  task_completed_at = models.CharField(max_length=255, blank=True, null=True)
  task_created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.task_name

  class Meta:
    ordering = ["task_invoice_date"]

  def save(self, *args, **kwargs):
    new_id = random.randint(100000000, 999999999)
    if not Task.objects.filter(id=self.id).exists():
      self.id = new_id
    super().save(*args, **kwargs)