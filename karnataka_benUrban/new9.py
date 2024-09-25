import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.support.ui import Select


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
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'btn1'))).click()

        # Wait for the results page to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.dataTables_scrollBody tbody')))

        # Locate the table body where the rows are present
        table_body = driver.find_element(By.CSS_SELECTOR, '.dataTables_scrollBody tbody')

        # Find all rows in the table
        rows = table_body.find_elements(By.TAG_NAME, 'tr')

        # List to hold all the "View Project Details" buttons
        view_details_buttons = []

        # Iterate over each row and find the "View Project Details" button
        for row in rows:
            try:
                # Find the "View Project Details" button in the 4th td
                view_details_td = row.find_elements(By.TAG_NAME, 'td')[3]
                view_details_button = view_details_td.find_element(By.CSS_SELECTOR, 'a[title="View Project Details"]')
                
                # Print the button's attributes
                print(f"Found button with ID: {view_details_button.get_attribute('id')}")
                print(f"Found button with title: {view_details_button.get_attribute('title')}")
                print(f"Found button with onclick: {view_details_button.get_attribute('onclick')}")
                
                # Store the button
                view_details_buttons.append(view_details_button)

            except Exception as e:
                print(f"An error occurred while finding a button: {e}")

        # List to hold all the scraped data
        all_data = []

        # Visit each "View Project Details" button separately
        for button in view_details_buttons:
            try:
                # Print the button before clicking
                print(f"Visiting button with ID: {button.get_attribute('id')}")
                
                # Click on the "View Project Details" button
                driver.execute_script("arguments[0].click();", button)

                # Wait for the Promoter Details tab to load
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div#home.active')))
                time.sleep(2)  # Give it extra time to ensure all elements are loaded

                # Scrape all relevant data from the promoter details
                data = []
                rows = driver.find_elements(By.CSS_SELECTOR, '.row')
                for row in rows:
                    columns = row.find_elements(By.CSS_SELECTOR, 'p')
                    if len(columns) >= 2:
                        label = columns[0].text.strip()
                        value = columns[1].text.strip()
                        data.append((label, value))

                all_data.append(data)

                # Go back to the results page
                driver.back()

                # Wait for the results page to load again
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.dataTables_scrollBody tbody')))
                time.sleep(2)

                # Re-locate the table body to handle any dynamic changes
                table_body = driver.find_element(By.CSS_SELECTOR, '.dataTables_scrollBody tbody')
                rows = table_body.find_elements(By.TAG_NAME, 'tr')

                # Re-locate the view_details_buttons list to handle any dynamic changes
                view_details_buttons = [row.find_elements(By.TAG_NAME, 'td')[3].find_element(By.CSS_SELECTOR, 'a[title="View Project Details"]') for row in rows]

            except Exception as e:
                print(f"An error occurred while processing a button: {e}")

        # Save the data to a CSV file
        with open('promoter_details.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Label", "Value"])  # Write headers
            for data in all_data:
                writer.writerows(data)

        print("Data scraped and saved to promoter_details.csv")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the WebDriver
        driver.quit()

# Example usage
url = 'https://rera.karnataka.gov.in/projectViewDetails'  # Replace with the actual URL
scrape_promoter_details(url)
