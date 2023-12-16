from rest_framework import serializers

from .models import ListOfHives, Hive, DataHive, DataHistory, Apiary
from authentication.serializers import *


class HiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hive
        fields = ('number', 'apiary')


class UpdateApiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Hive
        fields = ('id', 'apiary',)


class ListOfHivesSerializer(serializers.ModelSerializer):
    hive = HiveSerializer(read_only=True)

    class Meta:
        model = ListOfHives
        fields = ['hive']


class ApiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Apiary
        fields = '__all__'


class DataHiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataHive
        fields = '__all__'
