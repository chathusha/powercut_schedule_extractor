from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from datetime import datetime


def extract_data(url: str, path: str, group_name: str):
    """
    Extracts demand shedding data relevent to tommorow from the given url.
    :param url: url to extract data from
    :param path: path to webdriver
    :param group_name: name of the group in capital letters
    :return: data extracted from the url
    """
    driver = webdriver.Chrome(path)
    driver.get(url)

    next_day_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button[aria-label='next']")))
    next_day_btn.click()

    date_lbl = driver.find_element(By.CSS_SELECTOR, "h2").text
    date = datetime.strptime(date_lbl, "%B %d, %Y").date()

    time_data = [data.text for data in driver.find_elements(By.CLASS_NAME, "fc-content")]
    
    # TODO: extract start times and end times of each power cut

    # TODO: return the time data as a dictionary

    driver.quit()

    return {"date": date}