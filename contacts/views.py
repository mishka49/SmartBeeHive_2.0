from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from hives.models import Hive
# from .tasks import send_email_swarming


class SendMessageView(APIView):
    def get(self, request):
        # send_email_swarming.delay('andreym3ch@gmail.com', Hive.objects.first())
        return Response(status=status.HTTP_200_OK)
