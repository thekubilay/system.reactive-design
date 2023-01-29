import random

from django.db import models

class Setting(models.Model):
  invoice_text1 = models.CharField(max_length=255, null=True, blank=True)
  invoice_text2 = models.CharField(max_length=255, null=True, blank=True)
  invoice_text3 = models.CharField(max_length=255, null=True, blank=True)

  def save(self, *args, **kwargs):
    new_id = random.randint(100000000, 999999999)
    if not Setting.objects.filter(id=self.id).exists():
      self.id = new_id
    super().save(*args, **kwargs)
