"""Import required libraries for the tests"""
import time
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from configuration.config import driver_setup

""" TASK """

"""
URL: https://www.yavlena.com/broker/

Create automated test which cover the following:

Click on the “Зареди още“ button, this way on the page the brokers are loaded.
For each broker get the name of the broker, and search by the name of the broker.

On the search result view, make sure the searched broker is the only one displayed and make sure address,
2 phone numbers (landline, and mobile) and the number of properties assigned to the broker are displayed.

"""

def test_bugaboo():
    driver = driver_setup()
    WAIT = WebDriverWait(driver, 10)
    # Navigate to the form URL before any test cases
    driver.get(
        'https://service.bugaboo.com/s/consumer-contact?selectedItem=Consumer_Contact_Form__c&language=en_US')

    # Accept cookies button
    
    ac_cookies = WAIT.until(EC.element_to_be_clickable(
        (By.ID, 'CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll')))
    ac_cookies.click()

    # Wait for the combobox to be clickable
    # The ID seems to be dynamic, so we use Xpath to locate the object
    combobox_element = WAIT.until(EC.presence_of_element_located(
        (By.XPATH, "//button[contains(@class, 'slds-combobox__input') and contains(@class, 'slds-input_faux')]")))
    combobox_element.click()

    combobox_sub_el = WAIT.until(EC.presence_of_element_located(
        (By.XPATH, '//*[@data-value="General Question"]')))
    combobox_sub_el.click()

    next_btn = WAIT.until(
        EC.element_to_be_clickable((By.XPATH, "//lightning-button[@class='slds-button flow-button__NEXT']")))
    next_btn.click()

    description_field = WAIT.until(EC.presence_of_element_located(
        (By.XPATH, "//textarea[@id='input-82']")))
    description_field.send_keys("Test description, Veni, Vidi, Vici!")

    first_name = WAIT.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@id='input-86']")))
    first_name.send_keys("John")

    last_name = WAIT.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@id='input-90']")))
    last_name.send_keys("Wick")

    email = WAIT.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@id='input-94']")))
    email.send_keys("Example@gmail.com")

    verify_email = WAIT.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@id='input-98']")))
    verify_email.send_keys("Example@gmail.com")

    phone_number = driver.find_element(
        By.XPATH, "//input[@class='slds-input slds-form-element' and @type='tel' and @data-id='countryPhone']")
    driver.execute_script(
        "arguments[0].value = arguments[1];", phone_number, "2015558951")

    country = Select(driver.find_element(
        By.XPATH, "//select[@id='select-101']"))
    country.select_by_visible_text("United States")

    submit_form = driver.find_element(
        By.XPATH, "//button[normalize-space()='Next']")
    submit_form.click()
    assert WAIT.until(EC.presence_of_element_located(
        (By.XPATH, "//span[normalize-space()='Please complete the captcha']"))), "Submit failed"

    driver.quit()