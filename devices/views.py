from django.shortcuts import render
from rest_framework import status
from detector.services import Detector
from rest_framework.views import APIView
from devices.serializers import DeviceDataSerializer
from rest_framework.response import Response

from devices.services import Device
from hives.models import Hive, DataHive


class DeviceDataView(APIView):
    serializer_class = DeviceDataSerializer

    def post(self, request):
        serializer = DeviceDataSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):

            if (datahive := Device.create_datahive_instance(serializer.validated_data)) is not None:
                Detector.check_critical_situations(datahive)
                return Response(status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)
