from django.urls import path
# from .consumers import *
from . import consumers

websocket_urlpatterns = [
    # path('chat/', ChatConsumer.as_asgi()),
    path('chat/', consumers.ChatConsumer.as_asgi()),
]