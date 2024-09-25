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
    driver = webdriver.Chrome()

    all_data = []  # List to hold all the scraped data

    try:
        driver.get(url)

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, 'projectDist'))
        )

        district_dropdown = Select(driver.find_element(By.ID, 'projectDist'))
        district_dropdown.select_by_visible_text('Bengaluru Urban')

        time.sleep(2)  # Adjust if necessary

        search_button = driver.find_element(By.NAME, 'btn1')
        driver.execute_script("arguments[0].scrollIntoView(true);", search_button)

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, 'btn1'))
        ).click()

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.dataTables_scrollBody tbody'))
        )

        table_body = driver.find_element(By.CSS_SELECTOR, '.dataTables_scrollBody tbody')
        rows = table_body.find_elements(By.TAG_NAME, 'tr')

        total_buttons = len(rows)
        print(f"Total 'View Project Details' buttons found: {total_buttons}")

        # Iterate over each row
        for index in range(total_buttons):
            try:
                table_body = driver.find_element(By.CSS_SELECTOR, '.dataTables_scrollBody tbody')
                rows = table_body.find_elements(By.TAG_NAME, 'tr')

                row = rows[index]

                view_details_td = row.find_elements(By.TAG_NAME, 'td')[3]
                view_details_button = view_details_td.find_element(By.CSS_SELECTOR, 'a[title="View Project Details"]')

                print(f"\nClicking button {index + 1}/{total_buttons}:")
                print(f"ID: {view_details_button.get_attribute('id')}")
                print(f"Title: {view_details_button.get_attribute('title')}")

                driver.execute_script("arguments[0].scrollIntoView(true);", view_details_button)
                view_details_button.click()

                WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.ID, 'project_details_popup'))
                )
                print("Modal opened successfully.")

                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '#project_details_popup .inner_wrapper'))
                )

                modal = driver.find_element(By.ID, 'project_details_popup')
                data = {
                    "Promoter Name": "",
                    "Registration Number": "",
                    "PAN": "",
                    "GSTIN": "",
                    "District": "",
                    "Taluk": ""
                }

                modal_rows = modal.find_elements(By.CSS_SELECTOR, '.row')

                # Attempt to scrape available data without failing on missing elements
                for modal_row in modal_rows:
                    try:
                        cols = modal_row.find_elements(By.CSS_SELECTOR, 'div.col-md-3')
                        for i in range(0, len(cols), 2):
                            label_elem = cols[i].find_element(By.TAG_NAME, 'p')
                            value_elem = cols[i+1].find_element(By.TAG_NAME, 'p')

                            label = label_elem.text.strip().replace(':', '').lower()
                            value = value_elem.text.strip()

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
                    except (NoSuchElementException, IndexError):
                        # If any element is missing, skip and continue
                        continue

                # Add the data if at least one field is filled
                if any(data.values()):
                    all_data.append(data)
                    print(f"Scraped Data: {data}")
                else:
                    print("No data found in this modal.")

                close_button = modal.find_element(By.CSS_SELECTOR, 'button.close')
                close_button.click()

                WebDriverWait(driver, 10).until(
                    EC.invisibility_of_element_located((By.ID, 'project_details_popup'))
                )
                print("Modal closed successfully.")

                time.sleep(1)

            except (NoSuchElementException, TimeoutException, StaleElementReferenceException, IndexError) as e:
                print(f"An error occurred while processing button {index + 1}: {e}")
                continue

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
        driver.quit()

url = 'https://rera.karnataka.gov.in/projectViewDetails'  # Replace with the actual URL if different
scrape_promoter_details(url)
