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

try:
    # Open the URL
    url = "https://www.gujrera.gujarat.gov.in"  # Replace with the actual URL
    driver.get(url)

    # 1. Click on "Advanced"
    # advanced_button = WebDriverWait(driver, 30).until(
    #     EC.presence_of_element_located((By.ID, "details-button"))
    # )
    # advanced_button.click()

    # # 2. Click on "Proceed anyway"
    # proceed_button = WebDriverWait(driver, 30).until(
    #     EC.presence_of_element_located((By.ID, "proceed-link"))
    # )
    # proceed_button.click()

    # 3. Wait for the target element to load
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "DataFromJson"))
    )

    # Capture a screenshot to verify the page has loaded
    driver.save_screenshot("page_loaded.png")

    # 4. Locate and click the link
    registered_project_link = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(
            (By.XPATH, "//div[@id='DataFromJson']//a[@class='figur underlineData' and contains(text(), '14,675')]")
        )
    )
    driver.execute_script("arguments[0].click();", registered_project_link)

    # Optional: Add a delay to observe the result
    time.sleep(5)

    print("Successfully clicked the link.")

except Exception as e:
    print(f"Error: {e}")
    driver.save_screenshot("error_debug.png")
finally:
    driver.quit()
