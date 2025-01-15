from django.urls import path,reverse
from . import views
from django.shortcuts import redirect
from datetime import datetime
from django.conf import settings
from django.conf.urls.static import static
#define url patterns URLconf
urlpatterns = [path("index/",lambda request: redirect(reverse('index_view', kwargs={'month': datetime.now().month,'year': datetime.now().year}))),
               path("index/<int:month>/<int:year>/", views.index_view, name="index_view"),
               #path("appointment_data/", views.appointment_data, name= "appointment_data"),
               path("add_appointment/",views.add_appointment, name="add_appointment"),
               path("add_appointment/<int:year>/<int:month>/<int:day>/",views.add_appointment, name="add_appointment"),
               path("add_or_update_patient/",views.add_or_update_patient, name="add_or_update_patient"),
               path("add_or_update_patient/<int:patient_id>",views.add_or_update_patient, name="add_or_update_patient"),
               path("patient_list/",views.patient_list,name="patient_list"),
               path("patient_info/<int:patient_id>",views.patient_info,name="patient_info"),
               path("cancel_appointment/<int:appointment_id>",views.cancel_appointment, name="cancel_appointment")]
               #path('calendar/',views.calendar,name="calendar"),
               #path('create_event/',views.create_event,name="create_event"),
               #path('list_events/',views.list_events,name="list_events"),
               #path('oauth2callback/', views.oauth2callback, name='oauth2callback'),]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
