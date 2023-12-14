from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .repositories import ApiaryRepository
from .serializers import HiveSerializer, DataHiveSerializer, ListOfHivesSerializer, ApiarySerializer, \
    UpdateApiarySerializer

from .models import Hive, DataHive, ListOfHives, Apiary

from datetime import datetime, timedelta

from .services import DateTool, HiveService
from .tasks import beat_clear_outdated_data_from_model


class RegisterHiveView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = HiveSerializer

    def post(self, request):
        serializer = HiveSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            ListOfHives.objects.create(user=request.user, hive=serializer.instance)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UpdateHivesApiaryView(APIView):
    def patch(self, request):
        serializer = UpdateApiarySerializer(instance=Hive.objects.filter(id=request.data['id']))
        if serializer.is_valid():
            return Response(status=status.HTTP_202_ACCEPTED)
        return Response(status.HTTP_400_BAD_REQUEST)


class DataHiveView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, hive_id, last_days):
        if HiveService.is_user_owns_the_hive(user=request.user, hive=hive_id):
            data_hive = DataHive.objects.filter(hive=hive_id,
                                                date__range=DateTool.get_tuple_start_to_end_date(last_days))
            serializer = DataHiveSerializer(data_hive, many=True)
            return Response(serializer.data, status.HTTP_200_OK)

        return Response(status=status.HTTP_423_LOCKED)


class ListOfHivesView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ListOfHivesSerializer

    def get(self, request):
        user_hives = ListOfHives.objects.select_related("hive").filter(user=request.user)
        serializer = ListOfHivesSerializer(user_hives, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class HivesOfApiaryView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, apiary):
        user_hives = ListOfHives.objects.select_related("hive").filter(user=request.user, hive__apiary=apiary)
        serializer = ListOfHivesSerializer(user_hives, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiaryView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        apiaries = ApiaryRepository.users_apiaries(request.user)

        serializer = ApiarySerializer(apiaries, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ReportView(APIView):
    def get(self, request):
        from django.http import HttpResponse
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph
        from reportlab.lib.styles import getSampleStyleSheet

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="output.pdf"'
        doc = SimpleDocTemplate(response, pagesize=letter)
        styles = getSampleStyleSheet()
        lines = []
        text = "This is a multi-line text.\\nThis is the second line.\\nThis is the third line."
        for line in text.split("\\n"):
            lines.append(Paragraph(line, styles["Normal"]))
        doc.build(lines)
        return response
