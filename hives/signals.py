from django.db.models.signals import post_save, pre_delete, post_delete
from django.dispatch import receiver

from hives.models import DataHive, DataHistory


@receiver(post_delete, sender=DataHive)
def copy_data_to_history(sender, instance, **kwargs):
    data = DataHistory()

    data.hive_id = instance.hive_id
    data.weight = instance.weight
    data.temperature = instance.temperature
    data.humidity = instance.humidity
    data.date = instance.date
    data.is_swarming = instance.is_swarming
    data.is_robbed = instance.is_robbed
    data.is_robber = instance.is_robber
    data.save()
