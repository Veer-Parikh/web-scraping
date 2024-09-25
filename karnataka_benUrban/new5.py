from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
import time

def scrape_and_save_view_details(url):
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
        
        # Alternatively, click using JavaScript if regular click fails
        try:
            search_button.click()
        except:
            driver.execute_script("arguments[0].click();", search_button)

        # Wait for the results page to load
        time.sleep(5)

        # Locate the table body where the rows are present
        table_body = driver.find_element(By.CSS_SELECTOR, '.dataTables_scrollBody tbody')

        # Find all rows in the table
        rows = table_body.find_elements(By.TAG_NAME, 'tr')

        # Iterate over the rows and find the td with the title "View Project Details"
        for row in rows:
            try:
                # Find the "View Project Details" link in the 4th td
                view_details_td = row.find_elements(By.TAG_NAME, 'td')[3]
                view_details_link = view_details_td.find_element(By.CSS_SELECTOR, 'a[title="View Project Details"]')

                # Click on the "View Project Details" link
                view_details_link.click()

                # Wait for the new page to load
                time.sleep(5)

                # Save the loaded HTML page
                page_title = driver.title.replace(" ", "_").replace("/", "_")
                with open(f'{page_title}.html', 'w', encoding='utf-8') as file:
                    file.write(driver.page_source)
                print(f"HTML page saved successfully as {page_title}.html")

                # If needed, navigate back to the original page
                driver.back()

                # Wait before the next iteration
                time.sleep(2)

            except Exception as e:
                print(f"An error occurred while processing a row: {e}")

    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Close the WebDriver
        driver.quit()

# Example usage
url = 'https://rera.karnataka.gov.in/projectViewDetails'  # Replace with the actual URL
scrape_and_save_view_details(url)
