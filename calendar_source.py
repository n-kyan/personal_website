import streamlit as st
from msal import ConfidentialClientApplication
import requests, os
from datetime import datetime, timedelta

class OutlookCalendar:
    def __init__(self):

        # Get credentials from Streamlit secrets
        self.client_id = st.secrets['OUTLOOK_CLIENT_ID']
        self.tenant_id = st.secrets['OUTLOOK_TENANT_ID']
        self.client_secret = st.secrets['OUTLOOK_CLIENT_SECRET_VALUE']
        
        if not all([self.client_id, self.tenant_id, self.client_secret]):
            raise ValueError("Missing required secrets")
            
        self.authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        self.scope = ["https://graph.microsoft.com/.default"]

        # Set redirect URI based on environment
        # self.redirect_uri = ("http://localhost" if environment == "development" 
        #                    else "https://your-website.com/auth")
        
        # self.app = PublicClientApplication(
        #     client_id=self.client_id,
        #     authority=self.authority
        # )

    def get_token(self):
        app = ConfidentialClientApplication(
            client_id=self.client_id,
            client_credential=self.client_secret,
            authority=self.authority
        )

        result = app.acquire_token_for_client(scopes=self.scope)
        if not result.get('access_token'):
            raise Exception("Failed to acquire token")
        return result['access_token']

    def get_calendar_events(self, start_date=None, end_date=None):
        if not start_date:
            start_date = datetime.now()
        if not end_date:
            end_date = start_date + timedelta(days=7)

        token = self.get_token()
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        # Format dates for API
        start_str = start_date.isoformat() + 'Z'
        end_str = end_date.isoformat() + 'Z'

        url = f'https://graph.microsoft.com/v1.0/me/calendarView'
        params = {
            'startDateTime': start_str,
            'endDateTime': end_str,
            '$select': 'subject,start,end'
        }

        response = requests.get(url, headers=headers, params=params)
        return response.json()

    def create_meeting(self, meeting_details):
        token = self.get_token()
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        formatted_attendees = [
            {
                'emailAddress': {'address': email},
                'type': 'required'
            } for email in meeting_details['attendees']
        ]

        event = {
            'subject': meeting_details['subject'],
            'start': {
                'dateTime': meeting_details['start_time'].isoformat(),
                'timeZone': 'UTC'
            },
            'end': {
                'dateTime': meeting_details['end_time'].isoformat(),
                'timeZone': 'UTC'
            },
            'attendees': formatted_attendees,
            'body': {
                'content': meeting_details.get('description', ''),
                'contentType': 'text'
            }
        }

        if meeting_details.get('location'):
            event['location'] = {
                'displayName': meeting_details['location']
            }

        if meeting_details.get('is_online'):
            event['isOnlineMeeting'] = True
            event['onlineMeetingProvider'] = 'teamsForBusiness'

        url = 'https://graph.microsoft.com/v1.0/me/events'
        response = requests.post(url, headers=headers, json=event)
        return response.json()
    
    def display_events(self, events_data):
        """Format and display events in a readable way"""
        if not events_data.get('value'):
            return "No events found in this time period"
        
        formatted_events = []
        for event in events_data['value']:
            formatted_event = {
                'subject': event['subject'],
                'start': event['start']['dateTime'],
                'end': event['end']['dateTime'],
                'is_online': event['isOnlineMeeting'],
                'status': event['showAs']
            }
            formatted_events.append(formatted_event)
        
        return formatted_events
    
    def check_availability(self, date, duration_minutes=30):
        """Check availability for a specific date with given duration"""
        start_of_day = datetime.combine(date, datetime.min.time())
        end_of_day = datetime.combine(date, datetime.max.time())
        
        events = self.get_calendar_events(start_of_day, end_of_day)
        busy_periods = [(datetime.fromisoformat(e['start']['dateTime'].replace('Z', '')),
                        datetime.fromisoformat(e['end']['dateTime'].replace('Z', '')))
                    for e in events['value']]
        
        # Create time slots (example: 9 AM to 5 PM)
        available_slots = []
        current_time = start_of_day.replace(hour=9)  # Start at 9 AM
        end_time = start_of_day.replace(hour=17)     # End at 5 PM
        
        while current_time + timedelta(minutes=duration_minutes) <= end_time:
            slot_end = current_time + timedelta(minutes=duration_minutes)
            is_available = True
            
            for busy_start, busy_end in busy_periods:
                if not (slot_end <= busy_start or current_time >= busy_end):
                    is_available = False
                    break
            
            if is_available:
                available_slots.append({
                    'start': current_time,
                    'end': slot_end
                })
            
            current_time += timedelta(minutes=duration_minutes)
        
        return available_slots
