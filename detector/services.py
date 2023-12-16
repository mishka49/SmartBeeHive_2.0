import enum
from datetime import datetime
from typing import List

from DetectingMethods.function import FunctionTools
from detector.repositories import HiveDetectorRepository, CriticalSituationsRepository
from hives.models import Apiary, DataHive


class WeightStatus(enum.Enum):
    loss = 0
    normal = 1
    up = 2


class CriticalSituations(enum.Enum):
    swarming = 0
    robbed = 1
    robber = 2


class Weight:
    MAX_DEVIATION = 1
    SAMPLE_COUNT = 5

    def __init__(self):
        self.function = None
        self.status = WeightStatus.normal
        self.__max_deviation = self.MAX_DEVIATION
        self.is_created_function = False
        self.__sample_to_create_func = dict(time=[], weight=[])
        self.__step_of_create_function = int()

    def __add_data_to_sample(self, time: datetime, weight: float):
        self.__sample_to_create_func['time'].append(time)
        self.__sample_to_create_func['weight'].append(weight)

    def __reset(self):
        self.__sample_to_create_func['time'].clear()
        self.__sample_to_create_func['weight'].clear()
        self.__step_of_create_function = 0

    def update_status(self, value_time: datetime, value_weight: float):
        if self.function is not None:
            if FunctionTools.is_drastic_function_loss(self.function, value_time.timestamp(), value_weight,
                                                      self.__max_deviation):
                self.status = WeightStatus.loss
                self.is_created_function = False
                self.__reset()
                self.function = None

            elif FunctionTools.is_drastic_function_up(self.function, value_time.timestamp(), value_weight,
                                                      self.__max_deviation):
                self.status = WeightStatus.up
                self.is_created_function = False
                self.__reset()
                self.function = None

            else:
                self.status = WeightStatus.normal

        self.__update_function(value_time, value_weight)

    def __create_function(self, values_time: List[datetime], values_weight: List[float]):
        self.function = FunctionTools.approximation([t.timestamp() for t in values_time], values_weight,
                                                    lambda x, k, b: k * x + b)

    def __update_function(self, time: datetime, weight: float):
        if not self.is_created_function:
            self.__add_data_to_sample(time, weight)

            if len(self.__sample_to_create_func['time']) > 1:

                if self.__step_of_create_function < self.SAMPLE_COUNT - 1:
                    self.__create_function(self.__sample_to_create_func['time'],
                                           self.__sample_to_create_func['weight'])
                    self.__step_of_create_function += 1

                else:
                    self.__is_created_function = True
                    self.__reset()


class HiveDetector:
    def __init__(self):
        self.weight = Weight()

    def get_weight_status(self, time: datetime, weight: float):
        self.weight.update_status(time, weight)
        return self.weight.status

    def is_obj_changed(self):
        return not self.weight.is_created_function


class ApiaryDetector:
    @staticmethod
    def get_hives_with_weight_up(apiary: Apiary) -> List[HiveDetector]:
        print(f"START get_hives_with_weight_up")
        hives_with_weight_up = []

        for hive in HiveDetectorRepository.get_objects_from_common_apiary(apiary):
            if hive.weight.status is WeightStatus.up:
                hives_with_weight_up.append(hive)

        print(f"END get_hives_with_weight_up")
        return hives_with_weight_up


class Detector:
    @staticmethod
    def check_critical_situations(datahive: DataHive) -> None:
        print(f"START check_critical_situations")
        print(f"DATAHIVE: "
              f"hive: {datahive.hive}"
              f"weight: {datahive.weight}"
              f"time: {datahive.date}")
        critical_situations = list()

        is_swarming_or_theft = Detector.__check_swarming_or_theft(datahive)
        if is_swarming_or_theft is not None:
            critical_situations.append(is_swarming_or_theft)

        CriticalSituationsRepository.update(datahive.hive, Detector.__generate_dict(critical_situations))
        print(f"END check_critical_situations")

    @staticmethod
    def __generate_dict(critical_situations: List[CriticalSituations]) -> dict:
        critical_situations_dict = dict()
        for item in critical_situations:
            match item:
                case CriticalSituations.swarming:
                    critical_situations_dict['is_swarming'] = True
                case CriticalSituations.robbed:
                    critical_situations_dict['is_robbed'] = True
                case CriticalSituations.robber:
                    critical_situations_dict['is_robber'] = True

        return critical_situations_dict

    @staticmethod
    def __check_swarming_or_theft(datahive: DataHive) -> CriticalSituations:
        print(f"START check_swarming_or_theft")
        hive_detector = HiveDetectorRepository.get_obj(datahive.hive) or HiveDetector()
        weight_status = hive_detector.get_weight_status(datahive.date, datahive.weight)

        if hive_detector.is_obj_changed():
            HiveDetectorRepository.update_obj(datahive.hive, hive_detector)

        if weight_status == WeightStatus.loss:
            hives_with_weight_up = ApiaryDetector.get_hives_with_weight_up(datahive.hive.apiary)

            if len(hives_with_weight_up) != 0:
                print(f"end check_swarming_or_theft robbed")
                return CriticalSituations.robbed

            else:
                print(f"END check_swarming_or_theft swarming")
                return CriticalSituations.swarming

        if weight_status == WeightStatus.up:
            print(f"END check_swarming_or_theft robber")
            return CriticalSituations.robber
