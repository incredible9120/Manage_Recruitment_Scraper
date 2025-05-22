from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from geopy.geocoders import Nominatim
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

import json
import time
from numpy import random
import pandas as pd
import csv
import re


def escape_regex_chars(text):
    """
    Escape special regex characters in text
    """
    return re.escape(text)


# Setup
driver = webdriver.Chrome()
driver.get("https://www.ussportscamps.com/soccer/nike")
wait = WebDriverWait(driver, 3)

# Create/clear the comparison results file
with open("comparison_results.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["Details", "State", "Found In CSV"])
    writer.writeheader()

# Dictionary to store unique camps
camps_data = {}

dt_sections = driver.find_elements(By.TAG_NAME, "dt")
dd_sections = driver.find_elements(By.TAG_NAME, "dd")

# Read the CSV file once outside the loop
df = pd.read_csv("nike_soccer_camps_formatted.csv")

for section_index in range(len(dt_sections)):
    if section_index == 0:
        continue

    # Add random delay before scrolling
    time.sleep(random.randint(1, 2))
    dt_section = dt_sections[section_index]
    dd_section = dd_sections[section_index]

    # Scroll smoothly to the section
    driver.execute_script(
        "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
        dt_section,
    )

    state_name = dt_section.get_attribute("id")

    # Try to click safely with retries
    # if not safe_click_element(driver, dt_section):
    #     print(f"Failed to click state section {state_name}, skipping...")
    #     continue

    try:
        camp_sections = dd_section.find_elements(By.CLASS_NAME, "clearfix")

        for camp_section in camp_sections:
            try:
                link = (
                    camp_section.find_element(By.CLASS_NAME, "camps")
                    .find_element(By.TAG_NAME, "li")
                    .find_element(By.TAG_NAME, "a")
                )
                details = link.get_attribute("innerHTML")

                # Escape special regex characters in the details
                escaped_details = escape_regex_chars(details)

                # Check if camp exists in CSV using exact string matching
                found_in_csv = (
                    df["Event Details"]
                    .str.contains(escaped_details, case=False, regex=True)
                    .any()
                )

                # Record all camps with their status
                comparison_result = {
                    "Details": details,
                    "State": state_name,
                    "Found In CSV": "Yes" if found_in_csv else "No",
                }

                with open("comparison_results.csv", "a", newline="") as f:
                    writer = csv.DictWriter(
                        f, fieldnames=["Details", "State", "Found In CSV"]
                    )
                    writer.writerow(comparison_result)

            except Exception as e:
                print(f"Error processing camp in {state_name}: {str(e)}")
                continue

    except Exception as e:
        print(f"Error processing state {state_name}: {str(e)}")
        continue

print("Scraping completed. Data saved to comparison_results.csv")
driver.quit()
