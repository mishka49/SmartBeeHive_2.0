from datetime import datetime, timedelta

from authentication.models import User
from hives.models import Hive, ListOfHives
from hives.repositories import ApiaryRepository, HiveRepository, DataHiveRepository, WeatherRepository


class DateTool:
    def __init__(self, last_days: int, start_date=None, end_date=None):
        self.end_date = end_date or datetime.now()
        self.start_date = start_date or self.end_date - timedelta(last_days)

    def get_tuple_start_to_end_date(self):
        return self.start_date, self.end_date

    def get_parts_of_day_in_range(self, number_of_parts):
        dates = []
        for day in range((self.end_date - self.start_date).days):
            day = self.start_date + timedelta(day)
            for part in range(number_of_parts):
                dates.append(day + timedelta(seconds=24 * 60 * 60 * part / number_of_parts))

        return dates


class HiveService:
    @staticmethod
    def is_user_owns_the_hive(user: User, hive: Hive):
        return ListOfHives.objects.filter(user=user, hive=hive)


class ReportService:
    def __init__(self, last_days: int, user: User, quantity_per_day: int):
        self.user = user
        self.last_days = last_days
        self.quantity_per_day = quantity_per_day
        self.date_tool = DateTool(last_days, )
        self.parts_in_date_range = self.date_tool.get_parts_of_day_in_range(self.quantity_per_day)

    def __prepare_data(self, user: User) -> dict:
        apiaries = ApiaryRepository.users_apiaries(user)
        for apiary in apiaries:
            weather_records = [WeatherRepository.get_record_by_date(date, apiary) for date in
                               self.parts_in_date_range]

            for hive in HiveRepository.get_hives_from_apiary(apiary):
                data = DataHiveRepository.query_over_time(hive, self.date_tool.get_tuple_start_to_end_date())
                data = []


    def __generate_text(self, data: dict) -> str:
        pass

    def create_file(self, user):
        pass
