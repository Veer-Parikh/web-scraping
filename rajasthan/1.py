from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Initialize the WebDriver (ensure you set the correct path to your WebDriver)
driver = webdriver.Chrome()

try:
    # Step 1: Navigate to the website
    driver.get("https://rera.rajasthan.gov.in/ProjectSearch?Out=Y")
    
    # Maximize the browser window
    driver.maximize_window()

    # Step 2: Select "Jaipur" from the dropdown
    from selenium.webdriver.support.ui import Select
    district_dropdown = driver.find_element(By.ID, "DistrictId")
    select = Select(district_dropdown)
    select.select_by_visible_text("Jaipur")
    time.sleep(1)

    # Step 3: Click the "Search" button
    search_button = driver.find_element(By.ID, "btn_SearchProjectSubmit")
    search_button.click()
    time.sleep(5)  # Wait for the search results to load

    # Step 4: Scrape the "View" links
    # Locate the <a> tags with the "View" text
    view_links = driver.find_elements(By.XPATH, '//a[text()="View"]')

    # Extract the href attributes and store them in an array
    hrefs = [link.get_attribute('href') for link in view_links[:10]]  # Limit to the first 10 links

    # Print the scraped links
    print("Scraped Links:")
    for href in hrefs:
        print(href)

finally:
    # Close the WebDriver
    driver.quit()
