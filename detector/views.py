from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from detector.models import CriticalSituationsModel
from detector.repositories import CriticalSituationsRepository
# from detector.serializers import SwarmingHivesSerializer
from hives.models import Hive, ListOfHives
from hives.serializers import HiveSerializer
from hives.repositories import HiveRepository

class HivesWithCriticalSituationsView(APIView):
    permission_classes = (IsAuthenticated,)
    # serializer_class = SwarmingHivesSerializer()

    # def get(self, request):
    #     hives = CriticalSituationsRepository.get_hives(request.user)
    #
    #     serializer = SwarmingHivesSerializer(hives, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

class RobberHIvesView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = HiveSerializer

    def get(self, request):
        pass


class ResetCriticalSituationsView(APIView):
    pass






