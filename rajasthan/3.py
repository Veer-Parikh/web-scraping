from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

# Initialize the WebDriver
driver = webdriver.Chrome()

# Function to extract text safely
def get_text_or_empty(element):
    try:
        return element.text.strip()
    except:
        return ""

# Data storage
scraped_data = []

try:
    driver.maximize_window()

    # Step 1: Navigate to the website
    driver.get("https://rera.rajasthan.gov.in/ProjectSearch?Out=Y")  # Replace with the actual URL
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

    # Step 4: Scrape the first 10 "View" links
    view_links = driver.find_elements(By.XPATH, '//a[text()="View"]')
    hrefs_level_1 = [link.get_attribute('href') for link in view_links[:10]]  # Only first 10 links

    # Step 5: Visit each href from level 1 and collect the next set of links
    hrefs_level_2 = []  # To store the second-level links
    for href in hrefs_level_1:
        driver.get(href)
        time.sleep(3)  # Wait for the page to load

        # Locate the <tr> elements and extract only the <a> tags with "View Details" that follow "Updated 25/12/2024"
        nested_view_links = driver.find_elements(By.XPATH, '//tr[td[contains(text(), "Updated project details as on (12/25/2024)")]]//a[@title="View Details"]')
        hrefs_level_2 += [nested_link.get_attribute('href') for nested_link in nested_view_links]

    # Visit only the second-level links and scrape details
    for href in hrefs_level_2[:10]:  # Limit to the first 10 second-level links
        print(href)
        driver.get(href)
        time.sleep(3)  # Wait for the page to load

        # Scrape Organization Name and Type
        try:
            organization_table = driver.find_element(By.XPATH, '//table[contains(@class, "table-bordered") and .//th[contains(text(), "Organization")]]')
            org_name = get_text_or_empty(organization_table.find_element(By.XPATH, './/td[contains(text(), "Organization Name")]/following-sibling::td'))
            org_type = get_text_or_empty(organization_table.find_element(By.XPATH, './/td[contains(text(), "Organization Type")]/following-sibling::td'))
        except:
            org_name, org_type = "", ""

        # Scrape Organization Contact Details
        try:
            contact_table = driver.find_element(By.XPATH, '//table[contains(@class, "table-bordered") and .//th[contains(text(), "Organization Contact Details")]]')
            office_number = get_text_or_empty(contact_table.find_element(By.XPATH, './/td[contains(text(), "Office Number")]/following-sibling::td'))
            website_url = get_text_or_empty(contact_table.find_element(By.XPATH, './/td[contains(text(), "Website URL")]/following-sibling::td'))
        except:
            office_number, website_url = "", ""

        # Append the scraped data
        scraped_data.append({
            "organization_name": org_name,
            "organization_type": org_type,
            "office_number": office_number,
            "website_url": website_url
        })

    # Print the scraped data
    for data in scraped_data:
        print(data)

finally:
    # Close the WebDriver
    driver.quit()
