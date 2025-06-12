from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

def login(driver, uname, pword):
    """
    Automates login, navigation, and scraping of Phonesuite device data using Selenium.

    The script logs into the portal, navigates to the Devices tab, paginates through the
    table, extracts relevant device data, sorts unregistered devices to the top, saves
    it as an Excel file, and emails it.
    """
    # --- LOGIN ---
    try:
        time.sleep(2)  # Wait for page to load
        driver.find_element(By.NAME, "username").send_keys(uname)
        driver.find_element(By.NAME, "password").send_keys(pword)

        # Select 'Configurator' from the dropdown
        select_element = driver.find_element(By.ID, "product")
        Select(select_element).select_by_visible_text("Configurator")

        # Submit form
        driver.find_element(By.NAME, "Submit").click()

    except Exception as e:
        print(f"An unexpected error occurred during login: {e}")
        return