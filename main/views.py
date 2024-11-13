from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import Appointment
from django.contrib import messages
import calendar
from datetime import datetime,timedelta

# Create your views here.
#index page view
def index_view(request,year = datetime.now().year, month = datetime.now().month):
#intergrating todays appointment to the template
    today = datetime.now().date()
    tomorrow  = today + timedelta(days=1)
    todays_appointments = Appointment.objects.filter(day=today)
    tomorrow_appointments = Appointment.objects.filter(day=tomorrow)
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
def add_appointment(request):
    if request.method=="POST":
        date = request.POST.get('day')
        time  = request.POST.get('time')
        patient = request.POST.get('patient')
        notes = request.POST.get('notes')
        if Appointment.object.filter(day=date,time=time).exists():
            messages(request,"Appointment already set in this date")
            return redirect('add_appointment')
        else:
            new_appointment = Appointment(
                day = date,
                time = time,
                patient = patient,
                notes = notes
            )
            new_appointment.save()
            messages.success(request,"Appointment added successfully to calendar")
        return render(request,'addapontment.html')
            
        