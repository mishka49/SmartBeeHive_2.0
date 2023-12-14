from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from authentication.models import User


class Apiary(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название", null=True)

    class Meta:
        pass

    def __str__(self):
        return str(self.id)


class Hive(models.Model):
    number = models.CharField(max_length=15, verbose_name="Код", unique=True)
    coordinates = models.CharField(max_length=30, verbose_name="Координаты", null=True)
    apiary = models.ForeignKey('Apiary', on_delete=models.SET_NULL, verbose_name="Пасека", null=True)

    class Meta:
        pass

    def __str__(self):
        return str(self.id)


class DataHiveAbstractBase(models.Model):
    hive = models.ForeignKey('Hive', on_delete=models.CASCADE, verbose_name="Улей")
    coordinates = models.CharField(max_length=30, verbose_name="Координаты", null=True)
    date = models.DateTimeField(auto_now_add=True)
    weight = models.FloatField(verbose_name="Вес")
    temperature = models.FloatField(verbose_name="Температура")
    humidity = models.FloatField(verbose_name="Влажность")
    is_swarming = models.BooleanField(default=False, verbose_name="Роение")
    is_robber = models.BooleanField(default=False, verbose_name="Украли")
    is_robbed = models.BooleanField(default=False, verbose_name="Обокрали")

    class Meta:
        abstract = True


class DataHive(DataHiveAbstractBase):
    pass


class DataHistory(DataHiveAbstractBase):
    pass


class ListOfHives(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hive = models.ForeignKey('Hive', on_delete=models.CASCADE)


class Weather(models.Model):
    apiary = models.ForeignKey(Apiary, on_delete=models.CASCADE)
    date = models.DateTimeField(verbose_name='Дата')
    temperature = models.FloatField()
    humidity = models.FloatField()
    wind_speed = models.FloatField()
    pressure = models.FloatField()
    cloudiness = models.ForeignKey('Cloudiness', on_delete=models.SET_NULL)


class Cloudiness(models.Model):
    name = models.CharField(max_length=50, unique=True)
