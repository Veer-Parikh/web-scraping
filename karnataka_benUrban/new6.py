from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
import time

def scrape_and_print_links(url):
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
        search_button.click()

        # Wait for the results page to load
        time.sleep(5)

        # Locate the table body where the rows are present
        table_body = driver.find_element(By.CSS_SELECTOR, '.dataTables_scrollBody tbody')

        # Find all rows in the table
        rows = table_body.find_elements(By.TAG_NAME, 'tr')

        # Iterate over the rows
        for row in rows:
            # Identify if the row is odd or even
            row_class = row.get_attribute('class')
            row_type = 'odd' if 'odd' in row_class else 'even'
            
            # Find all td elements in the row
            tds = row.find_elements(By.TAG_NAME, 'td')
            if len(tds) > 3:  # Ensure there are at least 4 columns
                try:
                    # Print all td texts for debugging
                    for index, td in enumerate(tds):
                        print(f"TD {index} text: {td.text}")

                    # Find the "View Project Details" link in the 4th td using XPath
                    view_details_td = tds[3]
                    view_details_link = view_details_td.find_element(By.XPATH, './/a[@title="View Project Details"]')
                    link = view_details_link.get_attribute('href')
                    print(f"Link: {link}")
                except Exception as e:
                    print(f"Error finding link in this row: {e}")

            print(f"Row class: {row_type}")

    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Close the WebDriver
        driver.quit()

# Example usage
url = 'https://rera.karnataka.gov.in/projectViewDetails'  # Replace with the actual URL
scrape_and_print_links(url)
