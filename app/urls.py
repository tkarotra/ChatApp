from django.urls import path
from .views import *

urlpatterns = [
    path('chat/', Chat, name="chat"),
]