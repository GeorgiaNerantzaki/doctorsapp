from django.db import models
from django.urls import reverse

# Create your models here.
#define appointment model
class Appointment(models.Model):
    day = models.DateField('Day of the appointment', help_text = "Date of the appointment")
    time  = models.TimeField('Time of the appointment', help_text="Time of the appointment")
    patient = models.CharField('Patients full name',max_length=100, help_text="Patients full name")
    notes = models.TextField('Notes', help_text="Notes",max_length=200, blank=True,null=True)
    
    def __str__(self):
        return self.day


