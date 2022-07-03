from extractor import get_tomorrow_schedule
from google_calendar import GoogleCalendar

from datetime import timedelta

URL = "https://cebcare.ceb.lk/Incognito/DemandMgmtSchedule"
PATH = "C:/Users/ROG/Documents/04. Hobbies/01. Python/07. Automation/powercut_schedule_extractor/src/chromedriver.exe"
GROUP = "K"
CREDENTIAL_PATH = 'api_credentials.json'
CALENDAR_ID = 'e3n3atqsubspcbp9cem6vvc014@group.calendar.google.com'

if __name__ == "__main__":
    
    # summary of the calendar events
    summary = f"Power cut: Group {GROUP}"

    google_calendar = GoogleCalendar(CREDENTIAL_PATH)

    # get power cut schedules
    schedules = get_tomorrow_schedule(URL, PATH, GROUP)

    # get events
    start_time = schedules.get('start_times')[0].replace(hour=0, minute=0)
    end_time = start_time + timedelta(days=1)

    events = google_calendar.get_events(start_time=start_time, end_time=end_time, calendar_id=CALENDAR_ID)

    # delete similar events
    for event in events.get('items'):
        if event.get('summary') == summary:
            google_calendar.delete_event(event_id=event.get('id'), calendar_id=CALENDAR_ID)

    # insert events
    for start_time, end_time in zip(schedules["start_times"], schedules["end_times"]):
        google_calendar.insert_event(summary=summary, start_time=start_time, end_time=end_time, calendar_id=CALENDAR_ID)