from rest_framework import serializers
from hives.models import *


class DeviceDataSerializer(serializers.Serializer):
    number = serializers.CharField(max_length=15)
    weight = serializers.FloatField()
    temperature = serializers.FloatField()
    humidity = serializers.FloatField()
