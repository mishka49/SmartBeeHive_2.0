from hives.models import Hive, DataHive
from hives.repositories import DataHiveRepository


class Device:
    @staticmethod
    def create_datahive_instance(validated_data):
        if (hive := Hive.objects.get(number=validated_data['number'])) is not None:
            datahive = DataHive(
                hive=hive,
                weight=validated_data['weight'],
                temperature=validated_data['temperature'],
                humidity=validated_data['humidity']
            )

            datahive.save()

            return datahive
