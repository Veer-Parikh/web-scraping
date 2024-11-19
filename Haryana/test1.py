from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Set up the WebDriver
driver = webdriver.Chrome()

# Open the URL
url = 'https://haryanarera.gov.in/admincontrol/registered_projects/2'
driver.get(url)

# Initialize a list to store href values
hrefs = []
total_records = 856  # Total number of records to process
processed_records = 0  # Counter for processed rows

# Loop until all 856 rows are processed or pagination ends
while processed_records < total_records:
    # Find the table body
    try:
        table_body = driver.find_element(By.CSS_SELECTOR, 'div#compliant_hearing_wrapper tbody')
        rows = table_body.find_elements(By.CSS_SELECTOR, 'tr.odd, tr.even')
        print(f"Processing page... Found {len(rows)} rows.")
    except Exception as e:
        print(f"Error locating rows: {e}")
        break

    # Loop through each row and extract hrefs
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, 'td')
        for cell in cells:
            try:
                # Try to find an <a> tag inside the <td>
                link = cell.find_element(By.TAG_NAME, 'a')
                href = link.get_attribute('href')
                # Collect only unique and relevant hrefs
                if href and "project_preview_open" in href:
                    if href not in hrefs:
                        hrefs.append(href)
            except:
                # If no <a> tag is found, continue to the next cell
                continue
        processed_records += 1  # Increment the processed record count

    # Check if there is a "Next" button and if it is enabled
    try:
        next_button = driver.find_element(By.ID, 'compliant_hearing_next')
        if 'disabled' in next_button.get_attribute('class'):
            print("No more pages to process. Exiting...")
            break
        # Click the "Next" button to load the next page
        print("Navigating to the next page...")
        next_button.click()
        time.sleep(2)  # Wait for the page to load
    except Exception as e:
        print(f"Error navigating to the next page: {e}")
        break

# Convert the hrefs list into a Pandas DataFrame
df = pd.DataFrame(hrefs, columns=["URL"])

# Save the DataFrame to a CSV file
df.to_csv("project_preview_open_links.csv", index=False)

# Print a summary and the first 5 rows
print(f"CSV file created: project_preview_open_links.csv")
print(f"Total unique hrefs collected: {len(hrefs)}")
print(df.head())

# Quit the driver
driver.quit()
