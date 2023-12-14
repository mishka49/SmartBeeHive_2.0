from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterHiveView.as_view(), name='hive'),
    path('update_hives_apiary/', UpdateHivesApiaryView.as_view(), name='update_hives_apiary'),
    path('list/', ListOfHivesView.as_view(), name='list_of_hives'),
    path('data/<str:hive_id>/<int:last_days>', DataHiveView.as_view(), name='data_hive'),
    path('apiary/<int:apiary>', HivesOfApiaryView.as_view(), name='apiary'),
    path('apiaries/', ApiaryView.as_view(), name='apiaries'),
    path('report/', ReportView.as_view(), name='report'),
]
