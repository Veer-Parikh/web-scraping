import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time

def scrape_promoter_details(url):
    # Initialize the WebDriver (e.g., Chrome)
    driver = webdriver.Chrome()

    try:
        # Open the website
        driver.get(url)

        # Allow the page to load completely
        time.sleep(5)  # Adjust if necessary

        # Find the District dropdown by its ID and select "Bengaluru Urban"
        district_dropdown = Select(driver.find_element(By.ID, 'projectDist'))
        district_dropdown.select_by_visible_text('Bengaluru Urban')

        # Allow some time after selecting the district
        time.sleep(2)

        # Scroll the search button into view using JavaScript
        search_button = driver.find_element(By.NAME, 'btn1')
        driver.execute_script("arguments[0].scrollIntoView(true);", search_button)

        # Wait until the search button is clickable and click it
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'btn1')))

        # Click the search button
        search_button.click()

        # Wait for the results page to load
        time.sleep(5)

        # Locate the table body where the rows are present
        table_body = driver.find_element(By.CSS_SELECTOR, '.dataTables_scrollBody tbody')

        # Find the first row in the table (adjust if you need to scrape multiple rows)
        first_row = table_body.find_elements(By.TAG_NAME, 'tr')[0]

        # Find the "View Project Details" link in the 4th td
        view_details_td = first_row.find_elements(By.TAG_NAME, 'td')[3]
        view_details_link = view_details_td.find_element(By.CSS_SELECTOR, 'a[title="View Project Details"]')

        # Click on the "View Project Details" link
        view_details_link.click()

        # Wait for the Promoter Details tab to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div#home.active')))
        time.sleep(2)  # Give it extra time to ensure all elements are loaded

        
        # Save the data to a CSV file
        with open('promoter_details.csv', 'w', newline='') as file:
            writer = csv.writer(file)

        print("Data scraped and saved to promoter_details.csv")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the WebDriver
        driver.quit()

# Example usage
url = 'https://rera.karnataka.gov.in/projectViewDetails'  # Replace with the actual URL
scrape_promoter_details(url)
