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

    # Step 4: Scrape the first 10 "View" links
    view_links = driver.find_elements(By.XPATH, '//a[text()="View"]')
    hrefs_level_1 = [link.get_attribute('href') for link in view_links[:10]]  # First 10 links

    # Step 5: Visit each href and collect the next set of links
    hrefs_level_2 = []  # To store the new 10 links
    for href in hrefs_level_1:
        # Visit each link
        driver.get(href)
        time.sleep(3)  # Wait for the page to load

        # Locate the <tr> element and extract the nested <a> tag with "View Details" text
        nested_view_links = driver.find_element(By.XPATH, '//tr/td/a[@title="View Details"]')
        
        # Extract href attributes and store them
        # for nested_link in nested_view_links:
        hrefs_level_2.append(nested_view_links.get_attribute('href'))

    # Print the collected hrefs from the second layer
    print("Collected Links from Second Layer:")
    for link in hrefs_level_2:
        print(link)

finally:
    # Close the WebDriver
    driver.quit()
