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
               path("add_or_update_patient/",views.add_or_update_patient, name="add_or_update_patient"),
               path("patient_list/",views.patient_list,name="patient_list"),
               path('calendar/',views.calendar,name="calendar"),
               path('create_event/',views.create_event,name="create_event"),
               path('list_events/',views.list_events,name="list_events"),]