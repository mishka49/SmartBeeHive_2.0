from rest_framework import serializers

from hives.models import Hive


class HivesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hive
        fields = ['id']



