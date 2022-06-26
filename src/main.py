import extractor

url = "https://cebcare.ceb.lk/Incognito/DemandMgmtSchedule"
path = "C:/Users/ROG/Documents/04. Hobbies/01. Python/07. Automation/powercut_schedule_extractor/src/chromedriver.exe"

if __name__ == "__main__":
    extractor.extract_data(url=url, path=path, group_name="K")
