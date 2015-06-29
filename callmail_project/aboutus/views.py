import re
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

def Aboutusandroid(request):
    obj = StaticContents.objects.get(pk=6)
    return HttpResponse(obj.body)


def Privacyandroid(request):
    obj = StaticContents.objects.get(pk=5)
    return HttpResponse(obj.body)

def Termsandroid(request):
    obj = StaticContents.objects.get(pk=4)
    return HttpResponse(obj.body)


def Broswer(request):
    device = {}

    ua = request.META.get('HTTP_USER_AGENT', '').lower()

    if ua.find("iphone") > 0:
        device['iphone'] = "iphone" + re.search("iphone os (\d)", ua).groups(0)[0]

    if ua.find("ipad") > 0:
        device['ipad'] = "ipad"

    if ua.find("android") > 0:
        device['android'] = "android" + re.search("android (\d\.\d)", ua).groups(0)[0].translate(None, '.')

    return HttpResponse(device)
