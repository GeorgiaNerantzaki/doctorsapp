from django import forms
from .models import Appointment

class AddAppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['date','time','patient','notes']