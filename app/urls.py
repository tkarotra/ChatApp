from django.urls import path
from .views import *

urlpatterns = [
    path('', Login, name="login"),
    path('register/', Register, name="register"),
    path('logout/', Logout, name="logout"),
    path('chat/', Chat, name="chat"),
]