from django.db import models
from django.urls import reverse
from app.models import CustomUser

# Create your models here.
#define appointment model
class Appointment(models.Model):
    date = models.DateField('Day of the appointment', help_text = "Date of the appointment")
    time  = models.TimeField('Time of the appointment', help_text="Time of the appointment")
    patient = models.CharField('Patients full name',max_length=100, help_text="Patients full name")
    notes = models.TextField('Notes', help_text="Notes",max_length=200, blank=True,null=True)
    
    def __str__(self):
        return f"Appointment for {self.patient} on {self.date} at {self.time}"
    
#define patient model
class Patient(models.Model):
    full_name=models.CharField('Full Name',max_length=200,unique=True)
    age = models.IntegerField('Age')
    date_of_birth = models.DateField('Date of birth', help_text = "Date of birth")
    phone_number = models.CharField('Phone number',max_length=200)
    address = models.CharField('Address',max_length=200,default=None,null=True,blank=True)
    email = models.CharField('Email',max_length=200,unique=True)
    insurance_number = models.CharField('Insurance number',max_length=200,unique=True)
    current_medications = models.TextField('Current medications',help_text="Current medications")
    medication_history = models.TextField('Medication history',help_text="Medication history")
    health_status = models.CharField('Health status or diagnosis', max_length=200)
    symptoms = models.TextField('Symptoms', help_text="Symptoms")
    medical_history = models.TextField('Medical history', help_text="Medical history")
    document=models.FileField(upload_to='documents/', null=True, blank=True)
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE,default=None,null=True,blank=True)
    def __str__(self):
        return self.full_name
    
    
#define document model and the relationship with the patient
"""class Document(models.Model):
    filename = models.CharField('Filename',max_length=200)
    patient = models.ManyToManyField(Patient)
    def __str__(self):
        return self.filename"""

