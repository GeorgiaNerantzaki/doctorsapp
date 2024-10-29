from django.urls import path
from . import views

#define url patterns URLconf
urlpatterns = [path("", views.login, name = "login"),
               path("register/", views.register, name= "register"),]