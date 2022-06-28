import extractor

url = "https://cebcare.ceb.lk/Incognito/DemandMgmtSchedule"
path = "C:/Users/ROG/Documents/04. Hobbies/01. Python/07. Automation/powercut_schedule_extractor/src/chromedriver.exe"

if __name__ == "__main__":
    schedules = extractor.get_tomorrow_schedule(url, path, "K")
