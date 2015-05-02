from django.shortcuts import render
from django.http import HttpResponse
from .models import StaticContents

# Create your views here.

def Aboutus(request):
    obj = StaticContents.objects.get(pk=1)
    return HttpResponse(obj.body)


def Privacy(request):
    obj = StaticContents.objects.get(pk=2)
    return HttpResponse(obj.body)

def Terms(request):
    obj = StaticContents.objects.get(pk=3)
    return HttpResponse(obj.body)
