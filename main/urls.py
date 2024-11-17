from django.urls import path,reverse
from . import views
from django.shortcuts import redirect
from datetime import datetime
#define url patterns URLconf
urlpatterns = [path("index/",lambda request: redirect(reverse('index_view', kwargs={'year': datetime.now().year, 'month': datetime.now().month}))),
               path("index/<int:year>/<int:month>/", views.index_view, name="index_view"),
               #path("appointment_data/", views.appointment_data, name= "appointment_data"),
               path("add_appointment/",views.add_appointment, name="add_appointment"),
               path("add_appointment/<str:selected_date>/",views.add_appointment, name="add_appointment"),
               path("add_or_update_patient/",views.add_or_update_patient, name="add_or_update_patient"),]