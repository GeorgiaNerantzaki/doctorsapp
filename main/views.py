from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import Appointment,Patient, Document
from django.contrib import messages
import calendar
from datetime import datetime,timedelta
from .forms import AddPatientForm

# Create your views here.
#index page view
def index_view(request,year = datetime.now().year, month = datetime.now().month):
#intergrating todays appointment to the template
    today = datetime.now().date()
    tomorrow  = today + timedelta(days=1)
    todays_appointments = Appointment.objects.filter(date=today)
    tomorrow_appointments = Appointment.objects.filter(date=tomorrow)
    if todays_appointments is None:
        messages.error("There are no appointments today")
    if tomorrow_appointments is None:
        messages.error("There are no appointments tomorrow")
#generate the calendar
    cal = calendar.monthcalendar(year,month)
    month_name = calendar.month_name[month]
    context = {
        'year':year,
        'month':month,
        'month_name':month_name,
        'cal':cal,
        'todays_appointments':todays_appointments,
        'tomorrows_appointments':tomorrow_appointments,
    }
  
    return render(request,'index.html',context)

#retrieve all the callendar appointments
#def appointment_data(request):
 #   appointment = Appointment.objects.all()
  #  data = [{"date": f"{appointment.day}T{appointment.time}","patient":appointment.patient,"notes":appointment.notes}]
   # return JsonResponse(data,safe=False)
    #return  render(request,'index/html')

#add a new appointment
def add_appointment(request, selected_date = None):
    if request.method=="POST":
        date = request.POST.get('date')
        time  = request.POST.get('time')
        patient = request.POST.get('patient')
        notes = request.POST.get('notes')
        if Appointment.object.filter(date=date,time=time).exists():
            messages(request,"Appointment already set in this date")
            return redirect('add_appointment', selected_date=date)
        else:
            new_appointment = Appointment(
                date = date,
                time = time,
                patient = patient,
                notes = notes
            )
            new_appointment.save()
            messages.success(request,"Appointment added successfully to calendar")
        if selected_date:
            return redirect('add_appointment_with_date', selected_date=selected_date)
        return redirect('add_appointment')
    return render(request,'addappointment.html', {'selected_date':selected_date})

#add or update a patient
def add_or_update_patient(request):
    #form = AddPatientForm()
    if request.method=="POST":
        #form = AddPatientForm(request.POST,request.FILES)
        full_name = request.POST.get('full_name')
        age  = request.POST.get('age')
        date_of_birth = request.POST.get('date_of_birth')
        phone_number = request.POST.get('phone_number')
        insurance_number = request.POST.get('insurance_number')
        email  = request.POST.get('email')
        current_medications = request.POST.get('current_medications')
        medication_history  = request.POST.get('medication_history')
        health_status = request.POST.get('health_status')
        medical_history = request.POST.get('medical_history')
        document = request.FILES.get('document')
        if Patient.objects.filter(insurance_number=insurance_number).exists():
            messages.error('The patient already is registered')
        else:
            new_patient = Patient(full_name=full_name,
                                  age=age,date_of_birth=date_of_birth,
                                  phone_number=phone_number,
                                  insurance_number=insurance_number,
                                  email=email,
                                  current_medications=current_medications,
                                  medication_history=medication_history,
                                  health_status=health_status,
                                  medical_history=medical_history,
                                  document=document)
            new_patient.save()
            messages.success('New patient succassfully updated or added')
    return render(request,'addorupdatepatient.html')
            