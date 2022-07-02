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
    """

    SCOPES = ["https://www.googleapis.com/auth/calendar"]
    TOKEN_ID = 'api_token.json'

    # authentication
    def __init__(self, credentials_path: str) -> None:

        self.credentials_path = credentials_path
        self.creds = None

        if os.path.exists(self.TOKEN_ID):
            self.creds = Credentials.from_authorized_user_file(self.TOKEN_ID)

        if not self.creds or not self.creds.valid:

            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())

            else:
                self.flow = InstalledAppFlow.from_authorized_user_file(
                    credentials_path, self.SCOPES)
                self.creds = self.flow.run_local_server(port=0)

            with open(self.TOKEN_ID, 'w') as token:
                token.write(self.creds.to_json())

    # insert event
    def insert_event(self, summary: str, start_time: datetime, end_time: datetime, calendar_id: str = 'primary') -> str:
        """
        Creates an event in the Google calendar with given calendar ID.

        Args:
            summary (str): summary of the event.
            start_time (datetime): start time of the event.
            end_time (datetime): end time of the event.
            calendar_id (str): optional, google calender id, by default 'primary'.

        Returns:
            str: event id for the sucessful event creation.
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

            event = service.events().insert(calendarId=calendar_id, body=body).execute()

            return event.get('id')

        except HttpError as error:
            print(error)

    # get events
    def get_events(self, start_time: datetime, end_time: datetime, calendar_id: str = 'primary') -> dict:
        """
        Get events from Google calendar for the given calendar ID.

        Args:
            start_time (datetime): start time of the window of events.
            end_time (datetime): end time of the window of events.
            calendar_id (str): optional, google calender id, by default 'primary'.

        Return:
            dict: dictionary of available events.
        """

        try:
            service = build('calendar', 'v3', credentials=self.creds)

            event_results = service.events().list(calendarId=calendar_id, timeMin=start_time.isoformat()+'Z',
                                                  timeMax=end_time.isoformat()+'Z', singleEvents=True,  orderBy='startTime').execute()

            return event_results

        except HttpError as error:
            print(error)

    # delete event
    def delete_event(event_id: str, calendar_id: str = 'primary') -> None:
        """
        Delete an event from Google calendar for the given calendar ID and event ID.

        Args:
            event_id (str): 
        """
        pass


# test
start_time = datetime(year=2022, month=7, day=3)
end_time = datetime(year=2022, month=7, day=4)

if __name__ == '__main__':
    path = 'api_credentials.json'

    google_calender = GoogleCalendar(path)

    results = google_calender.get_events(start_time, end_time)

    # print(results)
    print(results.get('items')[0])
