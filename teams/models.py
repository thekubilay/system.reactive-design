import random

from django.db import models
from settings.models import Setting


class Team(models.Model):
  tid = models.BigIntegerField(null=True, blank=False)  # team id
  name = models.CharField(null=False, blank=False, max_length=255)
  full_name = models.CharField(null=True, blank=False, max_length=255)
  setting = models.ForeignKey(Setting, on_delete=models.CASCADE, null=True)

  def __str__(self):
    return self.name

  def save(self, *args, **kwargs):
    new_id = random.randint(100000000, 999999999)
    if not Team.objects.filter(id=self.id).exists():
      self.id = new_id
    super().save(*args, **kwargs)


class TeamFilter(models.Model):
  team = models.ForeignKey(Team, null=True, on_delete=models.CASCADE)
  keywords = models.CharField(max_length=40, null=True, blank=True, help_text="キーワードは分譲名の中にあるかどうか")

  def __str__(self):
    return self.keywords

  def save(self, *args, **kwargs):
    new_id = random.randint(100000000, 999999999)
    if not TeamFilter.objects.filter(id=self.id).exists():
      self.id = new_id
    super().save(*args, **kwargs)
