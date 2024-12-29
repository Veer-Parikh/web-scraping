from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up WebDriver options
chrome_options = Options()
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--ignore-ssl-errors")
driver = webdriver.Chrome(options=chrome_options)

# Open the URL
url = "https://www.gujrera.gujarat.gov.in"  # Replace with the target URL
driver.get(url)

# Handle "Advanced" and "Proceed anyway"

# Rest of your scraping logic here...

driver.quit()
