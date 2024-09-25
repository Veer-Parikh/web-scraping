import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    StaleElementReferenceException
)
import time

def scrape_promoter_details(url):
    # Initialize the WebDriver (ensure chromedriver is in your PATH)
    driver = webdriver.Chrome()

    # List to hold all the scraped data
    all_data = []

    try:
        # Open the website
        driver.get(url)

        # Allow the page to load completely
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, 'projectDist'))
        )

        # Select "Bengaluru Urban" from the District dropdown
        district_dropdown = Select(driver.find_element(By.ID, 'projectDist'))
        district_dropdown.select_by_visible_text('Bengaluru Urban')

        # Wait for the Taluk dropdown or any dependent elements to load
        time.sleep(2)  # Adjust if necessary

        # Scroll the search button into view using JavaScript
        search_button = driver.find_element(By.NAME, 'btn1')
        driver.execute_script("arguments[0].scrollIntoView(true);", search_button)

        # Wait until the search button is clickable and click it
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, 'btn1'))
        ).click()

        # Wait for the results table to load
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.dataTables_scrollBody tbody'))
        )

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
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '.dataTables_scrollBody tbody'))
                )
                table_body = driver.find_element(By.CSS_SELECTOR, '.dataTables_scrollBody tbody')
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

                # Allow some time for modal content to load
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '#project_details_popup .inner_wrapper'))
                )

                # Extract data from the modal
                modal = driver.find_element(By.ID, 'project_details_popup')
                data = {
                    "Promoter Name": "",
                    "Registration Number": "",
                    "PAN": "",
                    "GSTIN": "",
                    "District": "",
                    "Taluk": ""
                }

                # Locate all rows within the modal
                modal_rows = modal.find_elements(By.CSS_SELECTOR, '.row')

                for modal_row in modal_rows:
                    try:
                        # Each row contains 4 divs: label col, value col, label col, value col
                        cols = modal_row.find_elements(By.CSS_SELECTOR, 'div.col-md-3')
                        for i in range(0, len(cols), 2):
                            label_elem = cols[i].find_element(By.TAG_NAME, 'p')
                            value_elem = cols[i+1].find_element(By.TAG_NAME, 'p')

                            # Extract text and clean it
                            label = label_elem.text.strip().replace(':', '').lower()
                            value = value_elem.text.strip()

                            # Map labels to desired keys
                            if 'promoter name' in label:
                                data["Promoter Name"] = value
                            elif 'registration number' in label:
                                data["Registration Number"] = value
                            elif label == 'pan':
                                data["PAN"] = value
                            elif label == 'gstin':
                                data["GSTIN"] = value
                            elif label == 'district':
                                data["District"] = value
                            elif label == 'taluk':
                                data["Taluk"] = value
                    except NoSuchElementException:
                        # If structure differs or elements are missing
                        continue

                # Append the data if at least one field is filled
                if any(data.values()):
                    all_data.append(data)
                    print(f"Scraped Data: {data}")
                else:
                    print("No data found in this modal.")

                # Close the modal
                close_button = modal.find_element(By.CSS_SELECTOR, 'button.close')  # Update selector if needed
                close_button.click()

                # Wait for the modal to close
                WebDriverWait(driver, 10).until(
                    EC.invisibility_of_element_located((By.ID, 'project_details_popup'))
                )
                print("Modal closed successfully.")

                # Optional: Wait a bit before the next iteration
                time.sleep(1)

            except (NoSuchElementException, TimeoutException, StaleElementReferenceException) as e:
                print(f"An error occurred while processing button {index + 1}: {e}")
                # Optionally, you can skip to the next button or implement retry logic
                continue

        # Save the data to a CSV file
        with open('promoter_details.csv', 'w', newline='', encoding='utf-8') as file:
            fieldnames = ["Promoter Name", "Registration Number", "PAN", "GSTIN", "District", "Taluk"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for data in all_data:
                writer.writerow(data)

        print("\nData scraped and saved to promoter_details.csv")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the WebDriver
        driver.quit()

# Example usage
url = 'https://rera.karnataka.gov.in/projectViewDetails'  # Replace with the actual URL if different
scrape_promoter_details(url)
