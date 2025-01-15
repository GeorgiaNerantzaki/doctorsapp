from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
from .models import Appointment,Patient
from django.contrib import messages
from calendar import Calendar,month_name
from datetime import datetime,timedelta
from .forms import AddPatientForm
from .utils import get_calendar_service
import googleapiclient.errors
import logging
from django.contrib.auth.decorators import login_required
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import calendar
from collections import defaultdict
import os
from django.core.files.storage import default_storage 
from django.db import transaction, IntegrityError
# Create your views here.
#index page view
logger = logging.getLogger(__name__)

def index_view(request,  year=None,month=None ):
    if month is None:
        month=datetime.now().month
    if year is None:
        year=datetime.now().year
    # Debug calendar type
    logger.info(f"Calendar type: {type(calendar)}")
    
    # Integrating today's appointment into the template
    appointments_for_month = Appointment.objects.filter(
        date__year=year,
        date__month=month
    )
    appointments_by_day = defaultdict(list)
    for appointment in appointments_for_month:
        appointments_by_day[appointment.date.day].append(appointment)
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)
    todays_appointments = Appointment.objects.filter(date=today)
    tomorrow_appointments = Appointment.objects.filter(date=tomorrow)
    
    if not todays_appointments.exists():
        messages.error(request, "There are no appointments today")
    if not tomorrow_appointments.exists():
        messages.error(request, "There are no appointments tomorrow")
    
    # Generate the calendar
    try:
        cal = Calendar().monthdayscalendar(year, month)
        month_name_str = month_name[month]
    except AttributeError as e:
        logger.error(f"Error generating calendar: {e}")
        messages.error(request, "Error generating the calendar")
        cal = []
        month_name_str = "Unknown"
    
    context = {
        'year': year,
        'month': month,
        'month_name': month_name_str,
        'cal': cal,
        'todays_appointments': todays_appointments,
        'tomorrow_appointments': tomorrow_appointments,
        'appointments_by_day': dict(appointments_by_day),
    }
    today = datetime.today().date()
    tomorrow = today + timedelta(days=1)

    # Filter appointments for today and tomorrow
    today_appointments = Appointment.objects.filter(date=today)
    tomorrow_appointments = Appointment.objects.filter(date=tomorrow)
    appointments_data=[]

    # Add today's appointments to the data list
    for appointment in today_appointments:
        appointments_data.append({
            "date": f"{appointment.date}T{appointment.time}",
            "patient": appointment.patient,
            "notes": appointment.notes
        })


    return render(request, 'index.html', context)



#add a new appointment
def add_appointment(request,year=None, month=None, day=None,appointments=None):
    if not all([year,month,day]):
      year=datetime.now().year
      month=datetime.now().month
      day=datetime.now().day
    appointments = []
    
    selected_date = datetime(year,month,day)
    appointments = Appointment.objects.filter(date=selected_date).order_by('time')
    if request.method=="POST":
        date = request.POST.get('date')
        time  = request.POST.get('time')
        patient = request.POST.get('patient')
        notes = request.POST.get('notes')
        if Appointment.objects.filter(date=date,time=time).exists():
            messages(request,"Appointment already set in this date")
            return redirect('add_appointment')
        else:
            new_appointment = Appointment(
                date = date,
                time = time,
                patient = patient,
                notes = notes
            )
            new_appointment.save()
            messages.success(request,"Appointment added successfully to calendar")
        return redirect('add_appointment',year=year, month=month,day=day)
    return render(request,'addappointment.html',{'year':year,'month':month,'selected_date': selected_date,'appointments': appointments})

#cancel appointment
def cancel_appointment(request,appointment_id):
    year=datetime.now().year
    month=datetime.now().month
    appointment=get_object_or_404(Appointment, id=appointment_id)
    if request.method=="POST":
        appointment.delete()
        messages.success(request,'Appointment successfully canceled')
    return redirect('index_view',month=month,year=year)


#see patient details and contact info
def patient_info(request,patient_id):
    year=datetime.now().year
    month=datetime.now().month
    patient=get_object_or_404(Patient, id=patient_id)
    patient_details = {
        "id": patient.id,
        "full_name": patient.full_name,
        "email": patient.email,
        "phone_number": patient.phone_number,
        "address": patient.address,
        "age": patient.age,
        "date_of_birth":patient.date_of_birth,
        "insurance_number":patient.insurance_number,
        "current_medications":patient.current_medications,
        "medication_history":patient.medication_history,
        "health_status":patient.health_status,
        "symptoms":patient.symptoms,
        "medical_history":patient.medical_history,
        
    }
    return render(request, "patientinfo.html", {
        "patient": patient,
        "year": datetime.now().year,
        "month": datetime.now().month,
        "document_url":patient.document.url if patient.document else None,
    })

#add or update a patient
def add_or_update_patient(request,patient_id=None):
    year=datetime.now().year
    month=datetime.now().month
    patient = None
    if patient_id is not None:
        patient=get_object_or_404(Patient,id=patient_id)
        
    if request.method=="POST":
        full_name = request.POST.get('full_name')
        age  = request.POST.get('age')
        date_of_birth = request.POST.get('date_of_birth')
        phone_number = request.POST.get('phone_number')
        address=request.POST.get('address')
        email  = request.POST.get('email')
        insurance_number = request.POST.get('insurance_number')
        current_medications = request.POST.get('current_medications')
        medication_history  = request.POST.get('medication_history')
        health_status = request.POST.get('health_status')
        symptoms=request.POST.get('symptoms')
        medical_history = request.POST.get('medical_history')
        document = request.FILES.get('document')
        print(request.POST)
        print("FILES data:", request.FILES)
        if Patient.objects.filter(insurance_number=insurance_number).exists():
            messages.error(request,'The patient already is registered')
        else:
            try:
                with transaction.atomic():
                   new_patient = Patient(
                      full_name=full_name,
                      age=age,
                      date_of_birth=date_of_birth,
                      phone_number=phone_number,
                      address=address,
                      insurance_number=insurance_number,
                      email=email,
                      current_medications=current_medications,
                      medication_history=medication_history,
                      health_status=health_status,
                      symptoms=symptoms,
                      medical_history=medical_history,
                      document=document,
                      doctor=request.user
                     )
                transcaction.commit()
                print(f"Patient {new_patient.full_name} saved successfully.")
                messages.success(request, 'New patient successfully added')
            except ValidationError as e:
                print(f"Validation error: {e}")
                messages.error(request, 'There was an error saving the patient')
            except Exception as e:
                print(f"Error occurred: {e}")
                messages.error(request, 'An error occurred while saving the patient')

        return redirect('add_or_update_patient')
    return render(request,'addorupdatepatient.html',{'year':year,'month':month,'patient':patient})



#retrieving patients list from the database
@login_required
def patient_list(request):
    year=datetime.now().year
    month=datetime.now().month
    patients = Patient.objects.filter(doctor = request.user).all()
    return render(request,'patientlist.html',{'patients':patients,'year':year, 'month':month})
""""
SCOPES = ['https://www.googleapis.com/auth/calendar']


def generate_credentials():
    flow = InstalledAppFlow.from_client_secrets_file(
        'client_secret_186039699074-1jej1tivbf1qct6m0hgm2saal7tj7ggg.apps.googleusercontent.com.json',
        SCOPES
    )
    flow.redirect_uri = 'http://localhost:8000/oauth2callback/'
    creds = flow.run_local_server(port=8000)
   
    # Save the credentials to a file
    with open('authorized_user.json', 'w') as token:
        token.write(creds.to_json())
    print("Credentials saved to 'authorized_user.json'")

generate_credentials()



def get_calendar_service():
    creds = Credentials.from_authorized_user_file('client_secret_186039699074-1jej1tivbf1qct6m0hgm2saal7tj7ggg.apps.googleusercontent.com.json', ['https://www.googleapis.com/auth/calendar'])
    service = build('calendar', 'v3', credentials=creds)
    return service



def calendar(request):
    year=datetime.now().year
    month=datetime.now().month
    cal = Calendar().monthdayscalendar(year, month)

    # Fetch Google Calendar events
    service = get_calendar_service()
    start_of_month = datetime(year, month, 1).isoformat() + 'Z'
    end_of_month = (datetime(year, month + 1, 1) - timedelta(seconds=1)).isoformat() + 'Z'

    try:
        events_result = service.events().list(
            calendarId='primary',
            timeMin=start_of_month,
            timeMax=end_of_month,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])
    except Exception as e:
        events = []
    return render(request,'calendar.html',{'year':year,'month':month,'events':events})

def create_event(request):
    service = get_calendar_service()

    event = {
        'summary': 'Sample Event',
        'location': '123 Example St, City',
        'description': 'A sample event created through Django.',
        'start': {
            'dateTime': (datetime.now() + timedelta(days=1)).isoformat(),
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': (datetime.now() + timedelta(days=1, hours=1)).isoformat(),
            'timeZone': 'America/Los_Angeles',
        },
    }

    try:
        event = service.events().insert(calendarId='primary', body=event).execute()
        return redirect('calendar')
    except googleapiclient.errors.HttpError as error:
        return render(request, 'error.html', {'error': str(error)})

def list_events(request):
    service = get_calendar_service()
    now = datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])
    return render(request, 'events.html', {'events': events})

def delete_event(request, event_id):
    service = get_calendar_service()
    try:
        service.events().delete(calendarId='primary', eventId=event_id).execute()
        return redirect('list_events')
    except googleapiclient.errors.HttpError as error:
        return render(request, 'error.html', {'error': str(error)})"""

