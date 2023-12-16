from django.contrib import admin
from django.urls import path, include

from contacts.views import SendMessageView

urlpatterns = [
    path('send/', SendMessageView.as_view())
]
