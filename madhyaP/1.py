from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd
import time

# Initialize the WebDriver (replace 'chromedriver' with your WebDriver path)
driver = webdriver.Chrome()

# Navigate to the website
url = "https://www.rera.mp.gov.in/projects/"
driver.get(url)

# Wait for the page to load completely
time.sleep(5)

# Select 'Bhopal' from the district dropdown
district_dropdown = Select(driver.find_element(By.ID, "project_district_code"))
district_dropdown.select_by_visible_text("Indore")
time.sleep(2)  # Allow the page to update after selecting the district

# Click the 'Search' button
search_button = driver.find_element(By.ID, "btn_search")
search_button.click()
time.sleep(5)  # Allow the search results to load

# Select '100' from the results-per-page dropdown
results_dropdown = Select(driver.find_element(By.NAME, "example_length"))
results_dropdown.select_by_value("100")
time.sleep(5)  # Allow the page to update with 100 results

# Storage for all links
project_links = []

# Loop through all 8 pages
page_count = 1
while page_count <= 16:
    # Find all project links on the current page
    link_elements = driver.find_elements(By.XPATH, "//td[@class='text-center']/a[@class='btn btn-sm btn-round btn-warning']")
    for link in link_elements:
        project_links.append({"Page": page_count, "Link": link.get_attribute("href")})
    
    # Print progress
    print(f"Scraped Page {page_count}, Links Found: {len(link_elements)}")
    
    # Click the 'Next' button if not on the last page
    
    next_button = driver.find_element(By.ID, "example_next")
    next_button.click()
    time.sleep(5)  # Allow the next page to load
    page_count += 1

# Save links to a CSV using pandas
df = pd.DataFrame(project_links)
df.to_csv("project_links1.csv", index=False)

# Print completion message
print("Scraping complete. Links saved to 'project_links.csv'.")

# Close the browser
driver.quit()
