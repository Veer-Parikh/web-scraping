import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
import time

# Helper function to handle click retries
def click_with_retry(driver, element, retries=3):
    for attempt in range(retries):
        try:
            driver.execute_script("arguments[0].scrollIntoView(true);", element)  # Scroll to the element
            driver.execute_script("arguments[0].click();", element)  # Click using JavaScript
            return True
        except Exception as e:
            print(f"Attempt {attempt + 1} to click failed: {str(e)}")
            if attempt == retries - 1:
                return False
            time.sleep(1)  # Wait before retrying

# Refetch rows to avoid stale element exceptions
def refetch_rows(driver):
    table_body = driver.find_element(By.CSS_SELECTOR, '.dataTables_scrollBody tbody')
    return table_body.find_elements(By.TAG_NAME, 'tr')

def scrape_promoter_ceo_and_project_details(url):
    # Initialize WebDriver
    driver = webdriver.Chrome()
    all_data = []  # List to hold all the scraped data

    try:
        driver.get(url)

        # Wait for the district dropdown to be present
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, 'projectDist'))
        )

        # Select 'Bengaluru Urban' in the district dropdown
        district_dropdown = Select(driver.find_element(By.ID, 'projectDist'))
        district_dropdown.select_by_visible_text('Bengaluru Urban')

        # Click on the search button
        search_button = driver.find_element(By.NAME, 'btn1')
        click_with_retry(driver, search_button)

        # Wait for the table to load
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.dataTables_scrollBody tbody'))
        )

        # Find all rows in the table
        rows = refetch_rows(driver)
        total_buttons = len(rows)
        print(f"Total 'View Project Details' buttons found: {total_buttons}")

        # Iterate over each row
        for index in range(total_buttons):
            try:
                rows = refetch_rows(driver)  # Refetch rows at the beginning of each iteration
                row = rows[index]
                view_details_td = row.find_elements(By.TAG_NAME, 'td')[3]  # 4th column contains the button
                view_details_button = view_details_td.find_element(By.CSS_SELECTOR, 'a[title="View Project Details"]')

                print(f"\nClicking button {index + 1}/{total_buttons}:")

                # Click the 'View Project Details' button
                if not click_with_retry(driver, view_details_button):
                    print("Failed to click the button after multiple attempts. Skipping...")
                    continue

                # Wait for modal to open
                WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.ID, 'project_details_popup'))
                )
                print("Modal opened successfully.")

                modal = driver.find_element(By.ID, 'project_details_popup')
                data = {
                    "Promoter Name": "",
                    "Registration Number": "",
                    "PAN": "",
                    "GSTIN": "",
                    "District": "",
                    "Taluk": "",
                    "CEO/MD Name": "",
                    "Designation": "",
                    "CEO/MD PAN": "",
                    "DIN": "",
                    "Account Name": "",
                    "Bank Name": "",
                    "Total Area of Land (Sq Mtr)": "",
                    "Total Open Area (Sq Mtr)": "",
                    "Total Covered Area (Sq Mtr)": "",
                    "Total Built-up Area (Sq Mtr)": "",
                    "Total Carpet Area (Sq Mtr)": "",
                    "Total Plinth Area (Sq Mtr)": "",
                    "Area of Open Parking (Sq Mtr)": "",
                    "Area of Covered Parking (Sq Mtr)": "",
                    "Area of Garage (Sq Mtr)": "",
                    "Total Project Cost (INR)": "",
                    "Cost of Land (INR)": "",
                    "Estimated Cost of Construction (INR)": ""
                }

                # Scrape promoter and CEO/MD details from 'menu1'
                modal_rows = modal.find_elements(By.CSS_SELECTOR, '.row')

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
                            elif 'pan' in label:
                                data["PAN"] = value
                            elif 'gstin' in label:
                                data["GSTIN"] = value
                            elif 'district' in label:
                                data["District"] = value
                            elif 'taluk' in label:
                                data["Taluk"] = value
                            elif 'ceo' in label or 'md' in label:
                                data["CEO/MD Name"] = value
                            elif 'designation' in label:
                                data["Designation"] = value
                            elif 'din' in label:
                                data["DIN"] = value
                    except (NoSuchElementException, IndexError):
                        continue

                # Now switch to 'menu2' (Project Details) tab
                project_details_tab = driver.find_element(By.CSS_SELECTOR, 'a[href="#menu2"]')
                click_with_retry(driver, project_details_tab)

                # Wait for the project details to load
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, 'menu2'))
                )

                # Scrape project details
                project_modal_rows = driver.find_element(By.ID, 'menu2').find_elements(By.CSS_SELECTOR, '.row')

                for project_row in project_modal_rows:
                    try:
                        cols = project_row.find_elements(By.CSS_SELECTOR, 'div.col-md-3')
                        for i in range(0, len(cols), 2):
                            label_elem = cols[i].find_element(By.TAG_NAME, 'p')
                            value_elem = cols[i+1].find_element(By.TAG_NAME, 'p')

                            label = label_elem.text.strip().replace(':', '').lower()
                            value = value_elem.text.strip()

                            if 'total area of land' in label:
                                data["Total Area of Land (Sq Mtr)"] = value
                            elif 'total open area' in label:
                                data["Total Open Area (Sq Mtr)"] = value
                            elif 'total coverd area' in label:
                                data["Total Covered Area (Sq Mtr)"] = value
                            elif 'total built-up area' in label:
                                data["Total Built-up Area (Sq Mtr)"] = value
                            elif 'total carpet area' in label:
                                data["Total Carpet Area (Sq Mtr)"] = value
                            elif 'total plinth area' in label:
                                data["Total Plinth Area (Sq Mtr)"] = value
                            elif 'area of open parking' in label:
                                data["Area of Open Parking (Sq Mtr)"] = value
                            elif 'area of covered parking' in label:
                                data["Area of Covered Parking (Sq Mtr)"] = value
                            elif 'area of garage' in label:
                                data["Area of Garage (Sq Mtr)"] = value
                            elif 'total project cost' in label:
                                data["Total Project Cost (INR)"] = value
                            elif 'cost of land' in label:
                                data["Cost of Land (INR)"] = value
                            elif 'estimated cost of construction' in label:
                                data["Estimated Cost of Construction (INR)"] = value
                    except (NoSuchElementException, IndexError):
                        continue

                # Now switch to 'Bank Details' tab (menu4)
                bank_details_tab = driver.find_element(By.CSS_SELECTOR, 'a[href="#menu4"]')
                click_with_retry(driver, bank_details_tab)

                # Wait for the bank details to load
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, 'menu4'))
                )

                # Scrape bank details
                bank_modal_rows = driver.find_element(By.ID, 'menu4').find_elements(By.CSS_SELECTOR, '.row')

                for bank_row in bank_modal_rows:
                    try:
                        cols = bank_row.find_elements(By.CSS_SELECTOR, 'div.col-md-3')
                        for i in range(0, len(cols), 2):
                            label_elem = cols[i].find_element(By.TAG_NAME, 'p')
                            value_elem = cols[i+1].find_element(By.TAG_NAME, 'p')

                            label = label_elem.text.strip().replace(':', '').lower()
                            value = value_elem.text.strip()

                            if 'account name' in label:
                                data["Account Name"] = value
                            elif 'bank name' in label:
                                data["Bank Name"] = value
                    except (NoSuchElementException, IndexError):
                        continue

                all_data.append(data)

                # Close the modal
                close_button = driver.find_element(By.ID, 'closeModal')
                click_with_retry(driver, close_button)

            except (NoSuchElementException, TimeoutException, StaleElementReferenceException) as e:
                print(f"Error processing row {index + 1}: {str(e)}")
                continue

    finally:
        driver.quit()

    return all_data

# Save the scraped data into a CSV file
def save_to_csv(data, filename):
    if data:
        keys = data[0].keys()
        with open(filename, 'w', newline='', encoding='utf-8') as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)

# Usage example
url = "https://rera.karnataka.gov.in/projectViewDetails"  # Replace with the actual URL
scraped_data = scrape_promoter_ceo_and_project_details(url)
save_to_csv(scraped_data, 'scraped_data.csv')
