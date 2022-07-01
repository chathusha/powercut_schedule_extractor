from datetime import datetime
import os
import logging

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def create_event(title: str, start_time: datetime, end_time: datetime, cred_file: str, cal_id: str = 'primary'):
    """
    Creates an event in Google calender.

    :param title: title of the event.
    :type title: str
    :param start_time: start time of the event.
    :type start_time: datetime
    :param end_time: end time of the event.
    :type end_time: datetime
    :param cred_file: file path to the credential file.
    :type cred_file: str
    :param cal_id: optional, calender which the event needs to be created in, by default 'primary'.
    :type cal_id: str 
    """

    # setup the logging
    logger = logging.getLogger(__name__)

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '%(asctime)s - %(filename)s - %(levelname)s - %(message)s')

    file_handler = logging.FileHandler('error.log')
    file_handler.setLevel(logging.ERROR)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    # scopes needed to access the google calender
    SCOPES = ["https://www.googleapis.com/auth/calendar"]

    # authancialicate the user
    creds = None

    if os.path.exists("api_token.json"):
        creds = Credentials.from_authorized_user_file("api_token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                cred_file, SCOPES)
            creds = flow.run_local_server(port=0)

        with open("api_token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)
        # TODO: check the calender is available or not

        # call the google calender API to create an event
        body = {
            'summary': f'{title}',
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'Asia/Colombo'
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'Asia/Colombo'
            }
        }

        event = service.events().insert(calendarId=cal_id, body=body).execute()
        logger.info('Event created with ID: ' + event.get('id'))
        

    except HttpError as error:
        logger.exception(error)