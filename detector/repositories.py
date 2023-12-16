from typing import List

import dill

from authentication.models import User
from detector.models import HiveDetectorModel, CriticalSituationsModel
from hives.models import Hive, Apiary, DataHive, ListOfHives
from hives.repositories import HiveRepository


class HiveDetectorRepository:
    @staticmethod
    def get_obj(hive: Hive):
        hive_detector = HiveDetectorModel.objects.get(hive=hive)
        if len(hive_detector.obj) == 0:
            return None
        return dill.loads(hive_detector.obj)

    @staticmethod
    def update_obj(hive: Hive, obj: object) -> None:
        HiveDetectorModel.objects.filter(hive=hive).update(
            obj=dill.dumps(obj)
        )

    @staticmethod
    def get_objects_from_common_apiary(apiary: Apiary) -> list:
        hives = HiveDetectorModel.objects.filter(hive=HiveRepository.get_hives_from_apiary(apiary))
        return [dill.loads(hive.obj) for hive in hives]

    @staticmethod
    def init_hive_detector(hive: Hive, obj: object):
        HiveDetectorModel.objects.create(
            hive=hive,
            obj=dill.dumps(obj)
        )


class CriticalSituationsRepository:
    @staticmethod
    def update(hive: Hive, critical_situations_dict: dict) -> None:
        critical_situations = CriticalSituationsModel.objects.get(hive=hive)
        datahive = DataHive.objects.filter(hive=hive).last()

        for item in critical_situations_dict.items():
            match item[0]:
                case 'is_swarming':
                    critical_situations.is_swarming = True
                    datahive.is_swarming = True
                case 'is_robbed':
                    critical_situations.is_robbed = True
                    datahive.is_robbed = True
                case 'is_robber':
                    critical_situations.is_robber = True
                    datahive.is_robber = True

        critical_situations.save()
        datahive.save()

    @staticmethod
    def reset(hive: Hive) -> None:
        CriticalSituationsModel.objects.get(hive=hive).update(
            is_swarming=False,
            is_robber=False,
            is_robbed=False
        )

    @staticmethod
    def init_critical_situation_for_hive(hive: Hive):
        CriticalSituationsModel.objects.create(
            hive=hive
        )

    # @staticmethod
    # def get_hives(user: User):
    #     hives = [item.hive for item in ListOfHives.objects.select_related('hive').filter(user=user)]
    #
    #     result_hives = []
    #
    #     for hive in hives:
    #         situation=CriticalSituationsModel.objects.get(hive=hive)
    #
    #
    #             result_hives.append(hive)
    #
    #     return result_hives


