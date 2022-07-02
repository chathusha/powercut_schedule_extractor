import extractor
from create_event import create_event

URL = "https://cebcare.ceb.lk/Incognito/DemandMgmtSchedule"
PATH = "C:/Users/ROG/Documents/04. Hobbies/01. Python/07. Automation/powercut_schedule_extractor/src/chromedriver.exe"
GROUP = "K"
CRED_FILE = 'api_credentials.json'
CALENDAR_ID = 'e3n3atqsubspcbp9cem6vvc014@group.calendar.google.com'

if __name__ == "__main__":
    # get power cut schedules
    schedules = extractor.get_tomorrow_schedule(URL, PATH, GROUP)

    for start_time, end_time in zip(schedules["start_times"], schedules["end_times"]):
        
        create_event(title=f'Power cut: Group {GROUP}', start_time=start_time, end_time=end_time, cred_file=CRED_FILE, cal_id=CALENDAR_ID)
