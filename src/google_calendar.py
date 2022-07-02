from calendar import calendar
from datetime import datetime
import os
import logging

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class GoogleCalendar():
    """
    Calendar object with methods to manage a Google calender.

    Args:
        credential_path (str): pathe for the Google calendar API credentials file.
        calendar_id (str): optional, ID of the Google calendar, by default 'primary.
    """

    SCOPES = ["https://www.googleapis.com/auth/calendar"]
    TOKEN_ID = 'api_token.json'

    # authentication
    def __init__(self, credentials_path: str, calendar_id: str = 'primary') -> None:

        self.credentials_path = credentials_path
        self.calendar_id = calendar_id
        self.creds = None

        if os.path.exists(self.TOKEN_ID):
            self.creds = Credentials.from_authorized_user_file(self.TOKEN_ID)

        if not self.creds or not self.creds.valid:

            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())

            else:
                self.flow = InstalledAppFlow.from_authorized_user_file(credentials_path, self.SCOPES)
                self.creds = self.flow.run_local_server(port=0)

            with open(self.TOKEN_ID, 'w') as token:
                token.write(self.creds.to_json())

    # insert event
    def insert_event(self, summary: str, start_time: datetime, end_time: datetime) -> str:
        """
        Creates an event in the Google calendar with given calendar ID.

        Args:
            summary (str): summary of the event.
            start_time (datetime): start time of the event.
            end_time (datetime): end time of the event.

        Returns:
            str: event id for the sucessful event creation, empty string otherwise.
        """

        try:
            service = build('calendar', 'v3', credentials=self.creds)

            body = {
                'summary': f'{summary}',
                'start': {
                    'dateTime': start_time.isoformat(),
                    'timeZone': 'Asia/Colombo'
                },
                'end': {
                    'dateTime': end_time.isoformat(),
                    'timeZone': 'Asia/Colombo'
                }
            }

            event = service.events().insert(calendarId=self.calendar_id, body=body).execute()

            return event.get('id')

        except HttpError as error:
            print(error)

    # TODO: get events
    # TODO: delete event