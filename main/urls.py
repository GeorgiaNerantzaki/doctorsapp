from django.urls import path
from . import views

#define url patterns URLconf
urlpatterns = [path("index/", views.index_view, name = "index"),
               path("appointment_data/", views.appointment_data, name= "appointment data"),
               path("add_appointment/",views.add_appointment, name="schedule a appointment"),]