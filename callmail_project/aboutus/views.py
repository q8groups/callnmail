from django.shortcuts import render
from django.http import HttpResponse
from .models import StaticContents

# Create your views here.

def Aboutus(request):
    return HttpResponse("Hello World!")


def Privacy(request):
    return HttpResponse("Hello World!")

def Terms(request):
    return HttpResponse("Hello World!")
