import random

from django.db import models
from teams.models import Team

class Project(models.Model):
  team = models.ForeignKey(Team, on_delete=models.CASCADE)  # team id
  oid = models.IntegerField(null=True, blank=False)  # order id
  pid = models.BigIntegerField(null=True, blank=False)  # project id
  gid = models.CharField(max_length=50, null=True, blank=True)  # google analytics id
  name = models.CharField(null=False, blank=False, max_length=255)
  company_name = models.CharField(null=True, blank=True, max_length=255)
  archived = models.BooleanField(default=False, null=False, blank=False)

  def __str__(self):
    return self.name

  class Meta:
    ordering = ["oid"]

  def save(self, *args, **kwargs):
    new_id = random.randint(100000000, 999999999)
    if not Project.objects.filter(id=self.id).exists():
      self.id = new_id
    super().save(*args, **kwargs)
