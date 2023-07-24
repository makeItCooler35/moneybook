from django.db import models

# Create your models here.

class Categories(models.Model):
  mcc = models.PositiveIntegerField(blank=False)
  name = models.CharField(max_length=255, blank=False)

class Book(models.Model):
  category = models.ForeignKey(Categories, on_delete=models.PROTECT, default=None, blank=True, null=True)
  sum = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=True)
  bonus = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=True)
  description = models.CharField(max_length=255, blank=True)
  account = None
  time_at = models.DateTimeField(blank=False, null=False)