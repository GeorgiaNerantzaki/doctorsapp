from django import forms
from .models import Appointment,Patient

#form to add appointments
class AddAppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['date','time','patient','notes']
       
#form to add or update  patients       
class AddPatientForm(forms.ModelForm):
    class Meta:
        model_one = Patient
        fields = ['full_name','age','date_of_birth','phone_number','email','address','insurance_number','current_medication','medication_history','health_status','symptoms','medical_history','document']