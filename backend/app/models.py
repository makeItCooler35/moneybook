from django.db import models

# Create your models here.

class Categories(models.Model):
  mcc = models.PositiveIntegerField(blank=True, default=None)
  name = models.CharField(max_length=255, blank=False)
  parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
  is_folder = models.BooleanField(blank=True, default=False)
  class Meta:
    constraints = [
      models.CheckConstraint(
        check=~models.Q(id=models.F('parent')),
        name='%(app_label)s_%(class)s_id_is_not_same_parent',
      )
    ]

class Book(models.Model):
  category = models.ForeignKey(Categories, on_delete=models.PROTECT, default=None, blank=True, null=True)
  sum = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=True)
  bonus = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=True)
  description = models.CharField(max_length=255, blank=True)
  account = None
  time_at = models.DateTimeField(blank=False, null=False)