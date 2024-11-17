from django import forms
from .models import Appointment,Patient,Document

#form to add appointments
class AddAppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['date','time','patient','notes']
       
#form to add or update  patients       
class AddPatientForm(forms.ModelForm):
    class Meta:
        model_one = Patient
        model_two = Document
        fields = ['full_name','age','date_of_birth','phone_number','email','insurance_number','current_medication','medication_history','health_status','symptoms','medical_history','document']