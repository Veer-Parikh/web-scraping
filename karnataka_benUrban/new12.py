import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time

def verify_clicking_buttons(url):
    # Initialize the WebDriver (make sure the chromedriver is in your PATH)
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

        # Get the total number of "View Project Details" buttons
        total_buttons = len(rows)
        print(f"Total 'View Project Details' buttons found: {total_buttons}")

        # Iterate over each row by index to avoid stale element issues
        for index in range(total_buttons):
            try:
                # Re-locate the table body and rows to ensure they are fresh
                table_body = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '.dataTables_scrollBody tbody'))
                )
                rows = table_body.find_elements(By.TAG_NAME, 'tr')

                # Locate the specific row
                row = rows[index]

                # Find the "View Project Details" button in the 4th td
                view_details_td = row.find_elements(By.TAG_NAME, 'td')[3]
                view_details_button = view_details_td.find_element(By.CSS_SELECTOR, 'a[title="View Project Details"]')

                # Print the button's attributes for verification
                button_id = view_details_button.get_attribute('id')
                button_title = view_details_button.get_attribute('title')
                button_onclick = view_details_button.get_attribute('onclick')
                print(f"\nClicking button {index + 1}/{total_buttons}:")
                print(f"ID: {button_id}")
                print(f"Title: {button_title}")
                print(f"Onclick: {button_onclick}")

                # Scroll the button into view
                driver.execute_script("arguments[0].scrollIntoView(true);", view_details_button)

                # Click the "View Project Details" button
                view_details_button.click()

                # Wait for the modal to appear
                WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.ID, 'project_details_popup'))
                )
                print("Modal opened successfully.")

                # Optional: Wait a bit to see the modal
                time.sleep(2)

                # Close the modal
                close_button = driver.find_element(By.CSS_SELECTOR, '#project_details_popup button.close')
                close_button.click()

                # Wait for the modal to close
                WebDriverWait(driver, 10).until(
                    EC.invisibility_of_element_located((By.ID, 'project_details_popup'))
                )
                print("Modal closed successfully.")

                # Optional: Wait a bit before the next iteration
                time.sleep(1)

            except Exception as e:
                print(f"An error occurred while processing button {index + 1}: {e}")

        print("\nAll buttons have been clicked successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the WebDriver
        driver.quit()

# Example usage
url = 'https://rera.karnataka.gov.in/projectViewDetails'  # Replace with the actual URL if different
verify_clicking_buttons(url)
