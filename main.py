from dotenv import load_dotenv
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from modules.login import login
from modules.nav_to_tab import nav_to_tab
from modules.scrape_table import scrape_table
from modules.create_user import create_user
import time

# Load environment variables from .env file
load_dotenv(override=True)

# Get credentials and URL from environment variables
url: str = os.getenv('url')
uname: str = os.getenv('usern')
pword: str = os.getenv('pword')

tabnames: str = ["endpoint"]
scrape: bool = False
createuser: bool = True

# Configure Chrome options to run headless (no GUI)
options = Options()
#options.add_argument('--headless')             # Run browser in headless mode
options.add_argument('--disable-gpu')          # Disable GPU hardware acceleration (optional)
options.add_argument('--no-sandbox')           # Bypass OS security model (needed on some systems)
options.add_argument('--window-size=1920,1080')  # Set viewport size to avoid hidden elements

# 👇 Add this to ignore certificate errors
options.add_argument("--ignore-certificate-errors")
options.add_argument("--allow-insecure-localhost")

# Initialize WebDriver with headless configuration
driver = webdriver.Chrome(options=options)
driver.get(url)

def main():
    login(driver, uname, pword)
    time.sleep(1)
    if scrape:
        for tab in tabnames:
            nav_to_tab(driver, tab)
            time.sleep(1)
            scrape_table(driver, tab)
    if createuser:
        create_user(driver)
        time.sleep(10)
    
if __name__ == "__main__":
    main()