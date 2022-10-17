from django.urls import path, re_path

from .consumers import *

ws_urlpatterns = [
    path(r'ws/some_url', WSConsumerTransactions.as_asgi()),
]