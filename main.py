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

# Setup
driver = webdriver.Chrome()
driver.get(
    "https://www.ussportscamps.com/soccer/nike"
)  # Replace with the actual page URL

wait = WebDriverWait(driver, 3)  # Increased wait time for better reliability


def safe_back_navigation(driver, max_attempts=3):
    """
    Safely navigate back and ensure page loads properly
    """
    for attempt in range(max_attempts):
        try:
            driver.back()
            # Wait for a key element that indicates the page has loaded
            WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "dt"))
            )
            return True
        except (TimeoutException, StaleElementReferenceException) as e:
            if attempt == max_attempts - 1:
                print(f"Failed to navigate back after {max_attempts} attempts")
                return False
            time.sleep(2)  # Wait before retrying
    return False


def remove_announcement_bar(driver):
    """
    Attempt to remove the announcement bar that might interfere with clicking
    """
    try:
        # Try to find and remove the announcement bar using JavaScript
        driver.execute_script(
            """
            var announcementBar = document.querySelector('.announcementBar--content');
            if (announcementBar) {
                announcementBar.remove();
            }
        """
        )
    except Exception as e:
        print(f"Failed to remove announcement bar: {str(e)}")


def safe_click_element(driver, element, max_attempts=3):
    """
    Safely click an element with multiple attempts and fallback methods
    """
    for attempt in range(max_attempts):
        try:
            # First try: regular click
            element.click()
            return True
        except Exception as e:
            if attempt == max_attempts - 1:
                # Last attempt: try JavaScript click
                try:
                    driver.execute_script("arguments[0].click();", element)
                    return True
                except Exception as js_e:
                    print(f"Failed to click element after all attempts: {str(js_e)}")
                    return False
            time.sleep(1)  # Wait before retrying
    return False


# Dictionary to store unique camps
camps_data = {}

dt_sections = driver.find_elements(By.TAG_NAME, "dt")
dd_sections = driver.find_elements(By.TAG_NAME, "dd")

for section_index in range(len(dt_sections)):
    if section_index == 0:
        continue

    # Add random delay before scrolling
    time.sleep(random.randint(1, 2))
    dt_section = dt_sections[section_index]
    dd_section = dd_sections[section_index]

    driver.execute_script(
        "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
        dt_section,
    )

    state_name = dt_section.get_attribute("id")
    wait.until(EC.element_to_be_clickable(dt_section))
    dt_section.click()

    camp_sections = dd_section.find_elements(By.CLASS_NAME, "clearfix")

    for camp_section in camp_sections:
        try:
            city_name = camp_section.find_element(By.TAG_NAME, "h3").get_attribute(
                "innerHTML"
            )

            link = (
                camp_section.find_element(By.CLASS_NAME, "camps")
                .find_element(By.TAG_NAME, "li")
                .find_element(By.TAG_NAME, "a")
            )

            camp_name = link.get_attribute("innerHTML")

            # Create a unique identifier for the camp
            camp_id = f"{state_name}_{city_name}_{camp_name}"

            # Check if we've already processed this camp
            if camp_id not in camps_data:
                time.sleep(random.randint(1, 2))
                ActionChains(driver).move_to_element(link).perform()
                time.sleep(random.randint(1, 2))

                # Remove announcement bar before clicking
                remove_announcement_bar(driver)

                # Try to click safely
                if not safe_click_element(driver, link):
                    print(f"Failed to click link for camp {camp_id}, skipping...")
                    continue

                wait.until(
                    EC.presence_of_element_located((By.CLASS_NAME, "campSidebar"))
                )

                campSideBar = driver.find_element(By.CLASS_NAME, "campSidebar")
                geolocator = Nominatim(user_agent="MyApp")

                location = geolocator.geocode(city_name)

                # Store camp details only once
                camps_data[camp_id] = {
                    "state": state_name,
                    "city": city_name,
                    "camp_name": camp_name,
                    "latitude": location.latitude if location else None,
                    "longitude": location.longitude if location else None,
                    "sessions": [],
                }

                # Collect all sessions for this camp
                availability_opens = campSideBar.find_elements(
                    By.CLASS_NAME, "availability--open"
                )

                for availability_open in availability_opens:
                    period = availability_open.find_element(
                        By.CLASS_NAME, "header-add"
                    ).text
                    age_gender = availability_open.find_element(
                        By.CLASS_NAME, "session--gender"
                    ).text
                    gender = age_gender.split("|")[0].strip()
                    age = age_gender.split("|")[1].strip()

                    session_data = {
                        "period": period,
                        "gender": gender,
                        "age": age,
                        "subsessions": [],
                    }

                    try:
                        # First try to find the container of all program details
                        details_container = availability_open.find_element(
                            By.CLASS_NAME, "session--details"
                        )
                        if details_container:
                            # Find all program elements within the container
                            program_elements = details_container.find_elements(
                                By.CLASS_NAME, "session--program"
                            )
                            cost_elements = details_container.find_elements(
                                By.CLASS_NAME, "ca-drip"
                            )

                            # Process each program element
                            for idx, program_element in enumerate(program_elements):
                                try:
                                    skill_text = program_element.get_attribute(
                                        "innerHTML"
                                    )
                                    cost = (
                                        cost_elements[idx].get_attribute("innerHTML")
                                        if idx < len(cost_elements)
                                        else "N/A"
                                    )

                                    # Parse skill and type
                                    if "|" in skill_text:
                                        parts = skill_text.split("|")
                                        skill = parts[0].strip()
                                        type_val = (
                                            parts[1].strip() if len(parts) > 1 else ""
                                        )
                                    else:
                                        skill = skill_text.strip()
                                        type_val = ""

                                    subsession_data = {
                                        "skill": skill,
                                        "type": type_val,
                                        "cost": cost,
                                    }
                                    session_data["subsessions"].append(subsession_data)
                                except Exception as e:
                                    print(f"Error processing program element: {str(e)}")
                                    continue
                    except Exception as e:
                        print(f"Error finding session details: {str(e)}")

                    camps_data[camp_id]["sessions"].append(session_data)

                print(f"Added new camp: {json.dumps(camps_data[camp_id], indent=2)}")

                if not safe_back_navigation(driver):
                    print(
                        f"Failed to navigate back for {city_name}. Refreshing the page..."
                    )
                    driver.refresh()
                    wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "dt")))
            else:
                print(f"Camp {camp_id} already processed, skipping...")

        except Exception as e:
            print(f"Error processing camp in {city_name}: {str(e)}")
            if not safe_back_navigation(driver):
                print("Error recovery: Refreshing the page...")
                driver.refresh()
                wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "dt")))

# Save all camps data to a JSON file
with open("camps_data1.json", "w") as f:
    json.dump(camps_data, indent=2, fp=f)

print("Scraping completed. Data saved to camps_data.json")
driver.quit()
