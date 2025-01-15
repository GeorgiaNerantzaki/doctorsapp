from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

#define url patterns URLconf
urlpatterns = [path("", views.login_view, name = "login_view"),
               path("register/", views.register, name= "register"),
               path('logout/', auth_views.LogoutView.as_view(), name='logout'),]