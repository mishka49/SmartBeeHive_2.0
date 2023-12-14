from datetime import datetime

from django.db.models import QuerySet

from authentication.models import User
from hives.models import *


class HiveRepository:
    @staticmethod
    def get_hives_from_apiary(apiary: Apiary):
        hives = Hive.objects.select_related('hive').filter(apiary=apiary)

    @staticmethod
    def get_users_hives(user: User):
        return Hive.objects.filter(user=user)


class DataHiveRepository:
    @staticmethod
    def last_instance(hive: Hive):
        return DataHive.objects.filter(hive=hive).last()

    @staticmethod
    def query_over_time(hive: Hive, date_range: tuple):
        return DataHive.objects.filter(hive=hive, date__range=date_range)


class ApiaryRepository:
    @staticmethod
    def users_apiaries(user: User):
        user_hives = ListOfHives.objects.select_related("hive").filter(user=user)
        apiaries = set()

        for item in user_hives:
            apiaries.add(item.hive.apiary)

        return apiaries


class WeatherRepository:
    @staticmethod
    def get_record_by_date(date: datetime, apiary):
        records_for_day = Weather.objects.filter(apiary=apiary).filter(date__year=date.year,
                                                                       date__month=date.month,
                                                                       date__day=date.day)

        if not records_for_day.exist():
            return None

        records = records_for_day.filter(date__minute=date.minute)
        if records.exists():
            return WeatherRepository.__finding_the_nearest_record(date, records)

        records = records_for_day.filter(date__hour=date.hour)
        if records.exist():
            return WeatherRepository.__finding_the_nearest_record(date, records)

        return records_for_day

    @staticmethod
    def __finding_the_nearest_record(find_date: datetime, queryset: QuerySet[Weather]):
        past_delta_result = datetime

        if len(queryset) == 1:
            return queryset[0]

        for index, item in enumerate(queryset.order_by('date')):
            if index % 2 == 0:
                delta_item = abs(find_date - item.date)
                delta_next_item = abs(find_date - queryset[index + 1].date)

                if delta_item > delta_next_item:
                    past_delta_result = delta_next_item
                    continue

                return min(past_delta_result, delta_item)

        return past_delta_result
