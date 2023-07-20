"""Import required libraries for the tests"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
from configuration.config import driver_setup

""" TASK """

""""
Create automated test which cover the following:
Click on the “Зареди още“ button, this way on the page the brokers are loaded.
For each broker get the name of the broker, and search by the name of the broker.

On the search result view, make sure the searched broker is the only one displayed and make sure address, 2 phone numbers (landline, and mobile)
and the number of properties assigned to the broker are displayed.
"""

def test_yavlena():
    driver = driver_setup()
    WAIT = WebDriverWait(driver, 10)
    driver.get('https://www.yavlena.com/broker/')

    time.sleep(1)
    # Accept cookies button
    cookie_btn = WAIT.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, '.hide-cookies-message')))
    cookie_btn.click()
    # Click the Load More button
    load_more_btn = WAIT.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, '.green-btn.load-more-results-list')))
    load_more_btn.click()
    time.sleep(1)
    try:
        WAIT.until(EC.invisibility_of_element(
            (By.CSS_SELECTOR, '.brokers-loading')))
    except:
        assert False
    # Get all the broker cards, containing their info
    broker_cards = WAIT.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.name a')))
    broker_names = list(
        (lambda cards: [card.text for card in cards])(broker_cards))

    for name in broker_names:
        # Execute search
        search_box = driver.find_element(By.CSS_SELECTOR, '.input-search')
        search_box.clear()
        search_box.send_keys(name)
        time.sleep(1)

        # Wait for the element to dissapear
        try:
            WAIT.until(EC.invisibility_of_element(
                (By.CSS_SELECTOR, '.brokers-loading')))
        except:
            assert False
        # Number of brokers displayed
        brokers_displayed = driver.find_elements(
            By.CSS_SELECTOR, '.broker-list-holder')
        assert len(
            brokers_displayed) == 1, f'Expected brokers to be 1, Actual: {len(brokers_displayed)}'

        # Broker name test
        result_name = driver.find_element(
            By.CSS_SELECTOR, '.broker-data .name a')
        assert name == result_name.text, f'Expected broker name to be {name}, \
                                                           Actual: {result_name.text}'
        # Broker address test
        broker_address = driver.find_element(
            By.CSS_SELECTOR, '.broker-data .office')
        assert len(
            broker_address.text) > 0, f'Expected broker address to be more than 0, Actual: {len(broker_address.text)}'

        # Test the number of properties a broker has
        broker_properties = driver.find_element(
            By.CSS_SELECTOR, '.broker-data .position a')
        assert broker_properties.is_displayed, 'Expected broker properties to be displayed, Actual: Not Displayed!'

        # Test the number of phones a broker has
        broker_phones = driver.find_elements(
            By.CSS_SELECTOR, '.tel-group .tel > a')
        assert len(
            broker_phones) == 2, f'Expected broker phone number to be 2, Actual: {len(broker_phones)} Broker: {name}'

