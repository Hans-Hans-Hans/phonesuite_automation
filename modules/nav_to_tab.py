from selenium.webdriver.common.by import By

def nav_to_tab(driver, tabname: str):
    try: 
        driver.find_element(By.PARTIAL_LINK_TEXT, tabname.lower().capitalize()).click()
    except Exception as e:
        print(f"Tab with name {tabname} was not found: {e}")