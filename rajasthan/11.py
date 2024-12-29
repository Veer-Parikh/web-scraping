from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import pandas as pd

# Initialize WebDriver
driver = webdriver.Chrome()

# Main script
try:
    # Step 1: Navigate to the website
    driver.get("https://rera.rajasthan.gov.in/ProjectSearch?Out=Y")
    driver.maximize_window()
    time.sleep(2)

    # Step 2: Select "Jaipur" from the dropdown
    district_dropdown = driver.find_element(By.ID, "DistrictId")
    select = Select(district_dropdown)
    select.select_by_visible_text("Jaipur")
    time.sleep(1)

    # Step 3: Click the "Search" button
    search_button = driver.find_element(By.ID, "btn_SearchProjectSubmit")
    search_button.click()
    time.sleep(5)  # Wait for the search results to load

    # Data storage
    all_hrefs = []

    # Step 4: Get total number of pages
    pagination_buttons = driver.find_elements(By.CSS_SELECTOR, ".ds4u-pager-btn")
    total_pages = int(pagination_buttons[-1].get_attribute("data-p"))  # Get the last page number

    # Step 5: Loop through all pages
    for page_num in range(1, total_pages + 1):
        # Navigate to the specific page
        try:
            page_button = driver.find_element(By.CSS_SELECTOR, f'a[data-p="{page_num}"]')
            page_button.click()
            time.sleep(5)  # Wait for the page to load
        except Exception as e:
            print(f"Failed to navigate to page {page_num}: {e}")
            continue

        # Scrape the first 10 "View" links
        view_links = driver.find_elements(By.XPATH, '//a[text()="View"]')
        hrefs_level_1 = [link.get_attribute('href') for link in view_links[:10]]  # First 10 links on the current page
        all_hrefs.extend(hrefs_level_1)

        # Print progress
        print(f"Scraped {len(hrefs_level_1)} links from page {page_num}.")

    # Step 6: Save the links to a CSV file
    df = pd.DataFrame(all_hrefs, columns=["href"])
    df.to_csv("hrefs_level_1.csv", index=False)
    print("All hrefs saved to hrefs_level_1.csv.")

finally:
    # Close the WebDriver
    driver.quit()
