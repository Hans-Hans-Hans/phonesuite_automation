from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException

def scrape_table(driver, tabname: str):
    data = []

    # Define column parsers per tabname
    if tabname.lower() in ["user", "users"]:
        tabname = "user"
        def parse_row(cells):
            return {
                "username": cells[1].text.strip(),
                "name": cells[2].text.strip(),
                "auth_type": cells[3].text.strip(),
                "state": cells[4].text.strip(),
                "acl": cells[5].text.strip(),
                "forward": cells[6].text.strip()
            }
    
    elif tabname.lower() in ["guest", "guests"]:
        tabname = "guest"
        def parse_row(cells):
            return {
                "last_name": cells[1].text.strip(),
                "first_name": cells[2].text.strip(),
                "affiliation": cells[3].text.strip(),
                "vip?": cells[4].text.strip(),
                "current_room": cells[5].text.strip(),
                "did": cells[6].text.strip()
            }

    elif tabname.lower() in ["room", "rooms"]:
        tabname = "rooms"
        def parse_row(cells):
            return {
                "room_name": cells[1].text.strip(),
                "device": cells[2].text.strip(),
                "guest_room": cells[3].text.strip(),
                "guest_name": cells[4].text.strip(),
                "status": cells[5].text.strip()
            }

    elif tabname.lower() in ["device", "devices"]:
        tabname = "device"
        def parse_row(cells):
            return {
                #"device_id": cells[0].find_element(By.CSS_SELECTOR, 'input.dev_radio').get_attribute("value"),
                "dev_type": cells[1].text.strip(),
                "name": cells[2].text.strip(),
                "status": cells[3].text.strip(),
                "ip": cells[4].text.strip(),
                "port": cells[5].text.strip(),
                "description": cells[6].text.strip(),
                "assignments": cells[7].text.strip(),
                "pickup_grp": cells[8].text.strip(),
                "sla": cells[9].text.strip(),
                "is_trunk": cells[10].text.strip()
            }

    else:
        raise ValueError(f"Unsupported tabname: {tabname}")

    try:
        while True:
            # Wait for rows to load (handle empty tables)
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, f"#{tabname.lower()}_table tbody tr"))
                )
            except TimeoutException:
                print(f"No rows found in {tabname} table, or timeout.")
                break

            rows = driver.find_elements(By.CSS_SELECTOR, f"#{tabname.lower()}_table tbody tr")

            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                data.append(parse_row(cells))

            # Pagination next button
            try:
                next_button = driver.find_element(By.ID, f"{tabname.lower()}_table_next")
                classes = next_button.get_attribute("class")
                if "disabled" in classes or "ui-state-disabled" in classes:
                    print(f"Reached last page for {tabname}.")
                    break
                next_button.click()

                # Wait until page updates by waiting for staleness of previous rows
                WebDriverWait(driver, 10).until(EC.staleness_of(rows[0]))

            except (NoSuchElementException, ElementNotInteractableException) as e:
                print(f"Next button not found or not clickable: {e}")
                break

        print(f"Total {tabname} records scraped: {len(data)}")
        for item in data:
            print(item)

    except Exception as e:
        print(f"Error scraping {tabname}: {e}")