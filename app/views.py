from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def login(request):
    return HttpResponse("This is the login page")


def register(request):
    return HttpResponse("This is the register page")