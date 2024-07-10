from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Initialize the WebDriver (make sure you have the appropriate WebDriver installed, like chromedriver)
driver = webdriver.Chrome()

try:
    # Navigate to the URL
    driver.get("https://maharera.maharashtra.gov.in/projects-search-result")

    # Locate the input element for the project name/number
    number_input = driver.find_element(By.ID, "edit-project-name")

    # Enter the project number and submit the form
    number_input.send_keys("P51800034716")
    number_input.submit()

    # Find the view details link and get its href attribute
    view_details_link = driver.find_element(By.CSS_SELECTOR, "a.click-projectmodal.viewLink.targetBlankLink")
    link_url = view_details_link.get_attribute("href")

finally:
    # Close the initial driver instance
    driver.quit()

# Open a new driver instance to navigate to the fetched URL
new_driver = webdriver.Chrome()

try:
    # Navigate to the fetched URL
    new_driver.get(link_url)

    # Find the new link with class 'btn btn-xs btn-info'
    new_table = new_driver.find_element(By.CLASS_NAME, "table.table-bordered.table-responsive.table-striped")
    # Click the new link
    new_element = new_table.find_element(By.CLASS_NAME,"btn.btn-xs.btn-info")

    new_element.click()

    time.sleep(5)
    new_driver.quit()
finally:
    # Close the new driver instance after completing tasks
    new_driver.quit()