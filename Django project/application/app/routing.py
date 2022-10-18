from django.urls import path, re_path

from .consumers import *

ws_urlpatterns = [
    path('ws/', WSConsumerTransactions.as_asgi()),
]