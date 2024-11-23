from django.urls import path
from . import views

#define url patterns URLconf
urlpatterns = [path("", views.login_view, name = "login_view"),
               path("register/", views.register, name= "register"),]