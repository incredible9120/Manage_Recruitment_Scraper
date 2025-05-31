from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import os

# Format proxy with authentication
username = "upb7sw65uf"
password = "oa610luara"
host = "104.164.71.234"
port = "7777"

# 63613084 Mlj5394 223744 Aic Au0747898 2025-05-25 2025-11-25
# 71914888 LRS3329 133123 State Farm 5985142E2938 2025-05-29 2025-11-29
# titleNumber = "71914888"
# plateNumber = "LRS3329"
# odometer = "133123"
# companyName = "State Farm"
# policyNumber = "5985142E2938"

titleNumber = "80598171"
plateNumber = "RR264E"
odometer = "47848"
companyName = "State farm"
policyNumber = "570 0177-F14-38"

effectiveMonth = "12"
effectiveDay = "14"
effectiveYear = "2024"

expirationMonth = "06"
expirationDay = "14"
expirationYear = "2025"

proxy_url = f"http://{username}:{password}@{host}:{port}"

# set selenium-wire options to use the proxy
seleniumwire_options = {"proxy": {"http": proxy_url, "https": proxy_url}}

# set Chrome options to run in headless mode
options = Options()
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

    # titleNum.send_keys(titleNumber)
    driver.execute_script("arguments[0].value = arguments[1];", titleNum, titleNumber)
    # plateNum.send_keys(plateNumber)
    driver.execute_script("arguments[0].value = arguments[1];", plateNum, plateNumber)

    checkBox = driver.find_element(By.NAME, "certifiedLoginInd")
    checkBox.click()
    time.sleep(1)
    loginElement.click()
    time.sleep(5)

    while True:
        print("Waiting for checkbox to be clickable again...")
        try:
            new_checkbox = driver.find_element(By.NAME, "certifiedLoginInd")
            print(new_checkbox)
            if not new_checkbox.is_selected():
                new_checkbox.click()
            driver.find_element(By.NAME, "continueButtonV3").click()
            time.sleep(1)
        except:
            # If checkbox not found, we've moved to new page
            print("Checkbox not found - moved to next page")
            break

    # Step 3
    print("Waiting for no step 3...")
    noStep3 = WebDriverWait(driver, 60).until(  # Extended wait time
        EC.element_to_be_clickable((By.ID, "nextPageServices"))
    )
    print("Clicking no step 3...")
    noStep3.click()
    time.sleep(1)
    driver.find_element(By.NAME, "continueButton").click()

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
    oneYear = WebDriverWait(driver, 60).until(  # Extended wait time
        EC.element_to_be_clickable((By.ID, "tempTwoYearRenewalNo"))
    )
    time.sleep(1)
    oneYear.click()

    driver.execute_script(
        "arguments[0].value = arguments[1];",
        driver.find_element(By.NAME, "tempRenewalOdometer1"),
        odometer,
    )
    driver.execute_script(
        "arguments[0].value = arguments[1];",
        driver.find_element(By.NAME, "tempInsuranceCompanyName1"),
        companyName,
    )
    driver.execute_script(
        "arguments[0].value = arguments[1];",
        driver.find_element(By.NAME, "tempInsurancePolicyNum1"),
        policyNumber,
    )
    driver.execute_script(
        "arguments[0].value = arguments[1];",
        driver.find_element(By.NAME, "tempInsuranceEffMonth1"),
        effectiveMonth,
    )
    driver.execute_script(
        "arguments[0].value = arguments[1];",
        driver.find_element(By.NAME, "tempInsuranceEffDay1"),
        effectiveDay,
    )
    driver.execute_script(
        "arguments[0].value = arguments[1];",
        driver.find_element(By.NAME, "tempInsuranceEffYear1"),
        effectiveYear,
    )
    driver.execute_script(
        "arguments[0].value = arguments[1];",
        driver.find_element(By.NAME, "tempInsuranceExpMonth1"),
        expirationMonth,
    )
    driver.execute_script(
        "arguments[0].value = arguments[1];",
        driver.find_element(By.NAME, "tempInsuranceExpDay1"),
        expirationDay,
    )
    driver.execute_script(
        "arguments[0].value = arguments[1];",
        driver.find_element(By.NAME, "tempInsuranceExpYear1"),
        expirationYear,
    )

    # driver.find_element(By.NAME, "tempRenewalOdometer1").send_keys(odometer)
    # driver.find_element(By.NAME, "tempInsuranceCompanyName1").send_keys(companyName)
    # driver.find_element(By.NAME, "tempInsurancePolicyNum1").send_keys(policyNumber)
    # driver.find_element(By.NAME, "tempInsuranceEffMonth1").send_keys(effectiveMonth)
    # driver.find_element(By.NAME, "tempInsuranceEffDay1").send_keys(effectiveDay)
    # driver.find_element(By.NAME, "tempInsuranceEffYear1").send_keys(effectiveYear)
    # driver.find_element(By.NAME, "tempInsuranceExpMonth1").send_keys(expirationMonth)
    # driver.find_element(By.NAME, "tempInsuranceExpDay1").send_keys(expirationDay)
    # driver.find_element(By.NAME, "tempInsuranceExpYear1").send_keys(expirationYear)
    driver.find_element(By.ID, "tempInsuranceCertificationyes").click()
    driver.find_element(By.ID, "regCardCertifyChkbox").click()
    time.sleep(5)
    print("Scrolling to continue button Step 5...")
    driver.execute_script(
        "arguments[0].scrollIntoView(true);",
        driver.find_element(By.NAME, "continueButton"),
    )
    driver.find_element(By.NAME, "continueButton").click()

    # Step 6
    continueButton = WebDriverWait(driver, 60).until(  # Extended wait time
        EC.element_to_be_clickable((By.NAME, "continueButton"))
    )
    driver.find_element(By.ID, "tempVrDonateOdtfno").click()
    driver.find_element(By.ID, "tempVrDonateVtfno").click()
    driver.find_element(By.ID, "tempVrDonatePcrfno").click()
    driver.find_element(By.ID, "tempVrDonateKtfno").click()
    driver.find_element(By.ID, "tempVrDonatePbccno").click()
    driver.find_element(By.ID, "tempVrDonateCtfdno").click()

    time.sleep(3)
    # Re-find the continue button before scrolling and clicking
    continueButton = driver.find_element(By.NAME, "continueButton")
    driver.execute_script("arguments[0].scrollIntoView(true);", continueButton)
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "continueButton"))
    ).click()

    total_fee = WebDriverWait(driver, 60).until(  # Extended wait time
        EC.presence_of_element_located((By.CLASS_NAME, "global-fee-total"))
    )
    # Take screenshot of final page
    print("Taking final screenshot...")
    driver.save_screenshot("screenshots/final_page.png")

    print(f"Total fee: {total_fee.text}")
    time.sleep(5)

# id = nextPageServices name = continueButton
# id = nextPageRenewal name = continueButton
# id = tempTwoYearRenewalNo name = tempRenewalOdometer1 name = tempInsuranceCompanyName1 name = tempInsurancePolicyNum1 name = tempInsuranceEffMonth1 name = tempInsuranceEffDay1 name = tempInsuranceEffYear1
# name = tempInsuranceExpMonth1 name = tempInsuranceExpDay1 tempInsuranceExpYear1 id = tempInsuranceCertificationyes id = regCardCertifyChkbox name = continueButton
# name = tempVrDonateOdtf1 tempVrDonateVtf1 tempVrDonatePcrf1 tempVrDonateKtf1 tempVrDonatePbcc1 tempVrDonateCtfd1
# td class = global-fee-total
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    driver.quit()
