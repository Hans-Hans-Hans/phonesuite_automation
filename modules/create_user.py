from modules.nav_to_tab import nav_to_tab
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.support.ui import Select
import time
import pandas as pd

df = pd.read_excel("user_template.xlsx", sheet_name="Sheet1", engine="openpyxl")

def create_user(driver):
    nav_to_tab(driver, "user")
    
    print(df.columns)
    
    for _, row in df.iterrows():
        # Click the "Add User" button (replace with actual selector)
        try:
            add_user_button = driver.find_element(By.LINK_TEXT, "Add User")
            add_user_button.click()
        except NoSuchElementException:
            print("Could not find the 'Add User' button.")
            break

        #time.sleep(2)  # Wait for form to load — adjust if needed

        # Fill out the user form
        driver.find_element(By.NAME, "usernam").send_keys(row["username"])
        driver.find_element(By.NAME, "firstnam").send_keys(row["firstname"])
        driver.find_element(By.NAME, "passwd").send_keys(str(row["password"]))
        driver.find_element(By.NAME, "passwdc").send_keys(str(row["password"]))
        driver.find_element(By.NAME, "pin2").send_keys(str(row["pin"]))
        
        # Normalize the string from Excel
        wakeupcalls_value = str(row["wakeupcalls"]).strip().lower()
        # Check if it's a "truthy" value
        if wakeupcalls_value in ["true", "yes", "1"]:
            checkbox = driver.find_element(By.NAME, "can_create_campaigns")  # Replace with correct ID/name
            if not checkbox.is_selected():
                checkbox.click()
                
        # Normalize the string from Excel
        browserconsole_value = str(row["browserconsole"]).strip().lower()
        # Check if it's a "truthy" value
        if browserconsole_value in ["true", "yes", "1"]:
            checkbox = driver.find_element(By.NAME, "bc_phone")  # Replace with correct ID/name
            if not checkbox.is_selected():
                checkbox.click()
                
        # Normalize the string from Excel
        soundrecord_value = str(row["soundrecord"]).strip().lower()
        # Check if it's a "truthy" value
        if soundrecord_value in ["true", "yes", "1"]:
            checkbox = driver.find_element(By.NAME, "can_record_sounds")  # Replace with correct ID/name
            if not checkbox.is_selected():
                checkbox.click()
                
        #driver.find_element(By.NAME, "extension").send_keys(str(row["extension"]))
        extension_select_elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "add_extension_select"))
        )
        extension_select = Select(extension_select_elem)
        extension_select.select_by_visible_text("Add New")
        driver.find_element(By.NAME, "addExtension").send_keys(str(row["username"]))
        
        #driver.find_element(By.NAME, "voicemail").send_keys(str(row["voicemail"]))
        voicemail_value = str(row["voicemail"]).strip().lower()
        if voicemail_value in ["true", "yes", "1"]:
            pass
        else:
            checkbox = driver.find_element(By.NAME, "haveVoicemail")
            checkbox.click()
            driver.find_element(By.NAME, "timeout_exten").send_keys(str(row["gotoextension"]))

        add_device_select_elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "add_device_select"))
        )
        add_device_select = Select(add_device_select_elem)
        add_device_select.select_by_visible_text("Add New")
        driver.find_element(By.NAME, "device_nam").send_keys(str(row["devicename"]))
        driver.find_element(By.NAME, "eCNAM").send_keys(str(row["dispatchablelocation"]))
        driver.find_element(By.NAME, "secret2").send_keys(str(row["secret"]))
        driver.find_element(By.NAME, "sip_calllimit").clear()
        driver.find_element(By.NAME, "sip_calllimit").send_keys(str(row["calllimit"]))

        # Click Submit/Save (replace selector as needed)
        #driver.find_element(By.ID, "submit-user-btn").click()

        print(f"User '{row['username']}' submitted.")
        driver.find_element(By.NAME, "action[viewusers]").click()

        #time.sleep(2)  # Wait for confirmation or return to the list before next loop
            