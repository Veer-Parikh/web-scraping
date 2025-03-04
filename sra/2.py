from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in background
driver = webdriver.Chrome(options=options)

# Open the website
URL = "https://sra.gov.in/details/our-projects"
driver.get(URL)

# Wait for the table to load
wait = WebDriverWait(driver, 15)

# CSV Setup
csv_file = "scraped_data.csv"
all_data = []

# Page Counter
page_number = 1
max_pages = 226  # Stop at page 226

while page_number <= max_pages:
    try:
        print(f"Scraping Page {page_number}...")

        # Wait for table to load
        table = wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))

        # Scroll down to ensure all data is loaded
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        # Extract headers (only on first page)
        if page_number == 1:
            headers = [th.text.strip() for th in table.find_elements(By.TAG_NAME, "th")]
            all_data.append(headers)  # Store headers in data list

        # Extract rows
        rows = table.find_elements(By.TAG_NAME, "tr")
        for row in rows[1:]:  # Skip header row
            columns = row.find_elements(By.TAG_NAME, "td")
            if columns:
                all_data.append([col.text.strip() for col in columns])

        print(f"Page {page_number} scraped successfully.")

        # Find and click the "Next Page" button using JavaScript
        try:
            next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Go to next page']")))
            driver.execute_script("arguments[0].click();", next_button)
            # print(f"Clicked Next Page {page_number} → {page_number + 1}")
            time.sleep(2)  # Allow new page to load
            page_number += 1

        except Exception as e:
            print(f"Next button not found or not clickable on page {page_number}. Stopping.")
            break

    except Exception as e:
        print(f"Error on page {page_number}: {e}")
        break

# Save data to CSV
with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(all_data)

print(f"Scraping completed! Data saved to {csv_file}")

# Close the browser
driver.quit()
