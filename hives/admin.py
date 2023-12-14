from django.contrib import admin
from .models import *


@admin.register(Hive)
class HiveAdmin(admin.ModelAdmin):
    list_display = ['number', 'apiary', 'coordinates']


@admin.register(Apiary)
class HiveAdmin(admin.ModelAdmin):
    list_display = ['id']


@admin.register(DataHive)
class DataHiveAdmin(admin.ModelAdmin):
    list_display = ['hive', 'date', 'weight', 'temperature', 'humidity']


@admin.register(DataHistory)
class DataHistoryAdmin(admin.ModelAdmin):
    list_display = ['hive', 'date', 'weight', 'temperature', 'humidity']


@admin.register(ListOfHives)
class HiveAdmin(admin.ModelAdmin):
    list_display = ['user', 'hive']
