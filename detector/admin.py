from django.contrib import admin

from detector.models import HiveDetectorModel, CriticalSituationsModel


@admin.register(HiveDetectorModel)
class HiveDetectorModelAdmin(admin.ModelAdmin):
    list_display = ['hive', 'obj']


@admin.register(CriticalSituationsModel)
class CriticalSituationsModelAdmin(admin.ModelAdmin):
    list_display = ['hive', 'is_swarming', 'is_robber', 'is_robbed']