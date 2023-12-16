from django.urls import path

from devices.views import DeviceDataView

urlpatterns = [
    path('send/', DeviceDataView.as_view(), name='device_send'),
]
