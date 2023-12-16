from django.db import models
from hives.models import Hive


class HiveDetectorModel(models.Model):
    hive = models.OneToOneField('hives.Hive', on_delete=models.CASCADE, primary_key=True)
    obj = models.BinaryField(max_length=5000)


class CriticalSituationsModel(models.Model):
    hive = models.OneToOneField('hives.Hive', on_delete=models.CASCADE, primary_key=True)
    is_swarming = models.BooleanField(default=False)
    is_robbed = models.BooleanField(default=False)
    is_robber = models.BooleanField(default=False)

    class Meta:
        pass


