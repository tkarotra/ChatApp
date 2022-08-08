from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *

# Create your views here.

def Chat(request):
    return render(request, "app/base.html")