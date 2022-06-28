from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from datetime import datetime


def get_tomorrow_schedule(url: str, path: str, group_name: str) -> dict:
    """
    Extracts demand shedding data relevent to tommorow from the given url.
    :param url: url to extract data from
    :param path: path to webdriver
    :param group_name: name of the group in capital letters
    :return: start times and end times of power cut schedules
    """
    driver = webdriver.Chrome(path)
    driver.get(url)

    # load the schedule for tommorow
    next_day_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button[aria-label='next']")))
    next_day_btn.click()

    date_lbl = driver.find_element(By.CSS_SELECTOR, "h2").text
    date = datetime.strptime(date_lbl, "%B %d, %Y").date()

    # extract powercut schedules from the CEB website
    schedules = [data.text for data in WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "fc-content")))]
    
    # extract start time and endtime of power cut schedules
    start_times = [datetime.strptime(schedule.split()[0], "%I:%M%p") for schedule in schedules if group_name in schedule]
    end_times = [datetime.strptime(schedule.split()[1], "%I:%M%p") for schedule in schedules if group_name in schedule]

    # replace date of start_times and end_times with extracted date
    start_times = [time.replace(year=date.year, month=date.month, day=date.day) for time in start_times]
    end_times = [time.replace(year=date.year, month=date.month, day=date.day) for time in end_times]

    driver.quit()

    return {"start_times": start_times, "end_times": end_times}