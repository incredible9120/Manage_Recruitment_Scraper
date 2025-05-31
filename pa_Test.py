from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import os
import tempfile

# Format proxy with authentication
username = "upb7sw65uf"
password = "oa610luara"
host = "104.164.71.234"
port = "7777"

proxy_url = f"http://{username}:{password}@{host}:{port}"

# set selenium-wire options to use the proxy
seleniumwire_options = {"proxy": {"http": proxy_url, "https": proxy_url}}

# set Chrome options to run in headless mode
options = Options()
temp_profile = tempfile.TemporaryDirectory()
options.add_argument(f"--user-data-dir={temp_profile.name}")
# options.add_argument("--headless=new")
options.add_argument("--window-size=1920,1080")
# initialize the Chrome driver with service, selenium-wire options, and chrome options
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    seleniumwire_options=seleniumwire_options,
    options=options,
)
os.makedirs("screenshots", exist_ok=True)

try:
    driver.get("https://www.pa.gov/services/dmv/renew-vehicle-registration.html")

    # Take screenshot of initial page
    print("Taking initial screenshot...")
    driver.save_screenshot("screenshots/initial_page.png")

    print("Waiting for button element...")
    element = WebDriverWait(driver, 45).until(
        EC.element_to_be_clickable((By.ID, "hero-a76cac28f5-button-1"))
    )
    href = element.get_attribute("href")
    print(f"Found button URL: {href}")

    # Execute JavaScript to scroll element into view before clicking
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    time.sleep(2)  # Small delay after scroll

    print("Clicking button and waiting for new tab...")
    original_window = driver.current_window_handle
    element.click()

    # Wait for new window/tab to appear and switch to it
    WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
    for window_handle in driver.window_handles:
        if window_handle != original_window:
            driver.switch_to.window(window_handle)
            break

    loginElement = WebDriverWait(driver, 60).until(  # Extended wait time
        EC.element_to_be_clickable((By.NAME, "continueButtonV3"))
    )

    titleNum = driver.find_element(By.NAME, "titleNum0")
    plateNum = driver.find_element(By.NAME, "tagNum0")

    # 85389447 MBZ5603
    # 64485058 Mly9815
    titleNum.send_keys("85389447")
    plateNum.send_keys("MBZ5603")

    checkBox = driver.find_element(By.NAME, "certifiedLoginInd")
    checkBox.click()
    time.sleep(1)
    loginElement.click()
    time.sleep(5)

    # Wait for and find the checkbox again after page load
    print("Waiting for checkbox to be clickable again...")
    new_checkbox = WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.NAME, "certifiedLoginInd"))
    )
    if new_checkbox.is_displayed():
        new_checkbox.click()
        driver.find_element(By.NAME, "continueButtonV3").click()
        time.sleep(5)

    # Step 3
    continueButton = WebDriverWait(driver, 60).until(  # Extended wait time
        EC.element_to_be_clickable((By.NAME, "continueButton"))
    )
    noStep3 = driver.find_element(By.ID, "nextPageServices")
    noStep3.click()
    time.sleep(1)
    continueButton.click()

    # Step 4

    # Add explicit wait for the radio button
    radioStep4 = WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.ID, "nextPageRenewal"))
    )
    # Add a small delay to ensure the page is stable
    time.sleep(2)
    # Try to click with JavaScript if normal click fails
    try:
        radioStep4.click()
    except:
        driver.execute_script("arguments[0].click();", radioStep4)
    time.sleep(1)
    driver.find_element(By.NAME, "continueButton").click()

    # Step 5
    continueButton = WebDriverWait(driver, 60).until(  # Extended wait time
        EC.element_to_be_clickable((By.NAME, "continueButton"))
    )
    oneYear = driver.find_element(By.ID, "tempTwoYearRenewalNo")
    time.sleep(1)
    oneYear.click()

    driver.find_element(By.NAME, "tempRenewalOdometer1").send_keys(odometer)
    driver.find_element(By.NAME, "tempInsuranceCompanyName1").send_keys(companyName)
    driver.find_element(By.NAME, "tempInsurancePolicyNum1").send_keys(policyNumber)
    time.sleep(1)
    driver.find_element(By.NAME, "tempInsuranceEffMonth1").send_keys(effectiveMonth)
    driver.find_element(By.NAME, "tempInsuranceEffDay1").send_keys(effectiveDay)
    driver.find_element(By.NAME, "tempInsuranceEffYear1").send_keys(effectiveYear)
    time.sleep(1)
    driver.find_element(By.NAME, "tempInsuranceExpMonth1").send_keys(expirationMonth)
    driver.find_element(By.NAME, "tempInsuranceExpDay1").send_keys(expirationDay)
    driver.find_element(By.NAME, "tempInsuranceExpYear1").send_keys(expirationYear)
    time.sleep(1)
    driver.find_element(By.ID, "tempInsuranceCertificationyes").click()
    driver.find_element(By.ID, "regCardCertifyChkbox").click()
    time.sleep(5)
    driver.execute_script("arguments[0].scrollIntoView(true);", continueButton)
    continueButton.click()

    # Take screenshot of final page
    print("Taking final screenshot...")
    driver.save_screenshot("screenshots/final_page.png")

    print(f"Final URL: {driver.current_url}")
    time.sleep(5)

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    driver.quit()
