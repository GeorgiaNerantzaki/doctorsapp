import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import os
from django.conf import settings
from google.oauth2.credentials import Credentials


SCOPES = ['https://www.googleapis.com/auth/calendar']


def get_calendar_service():
    credentials = Credentials.from_authorized_user_file('client_secret_1095938452235-agtcg272cs9noctrh4ah3dkei795kup5.apps.googleusercontent.com.json', SCOPES)
    service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)
    return service