from django.dispatch import receiver
from django.db.models.signals import post_init
from .repositories import HiveDetectorRepository, CriticalSituationsRepository
from .services import HiveDetector

from hives.models import Hive


@receiver(post_init, sender=Hive)
def create_hive_detector_for_hive(sender, instance, **kwargs):
    HiveDetectorRepository.init_hive_detector(instance, HiveDetector())


@receiver(post_init, sender=Hive)
def create_critical_situations_for_hive(sender, instance, **kwargs):
    CriticalSituationsRepository.init_critical_situation_for_hive(instance)
