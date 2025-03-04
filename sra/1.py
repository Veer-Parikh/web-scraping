from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Runs in background (remove for debugging)
driver = webdriver.Chrome(options=options)

# Open the website
URL = "https://sra.gov.in/details/our-projects"
driver.get(URL)

# Wait for the table to load
wait = WebDriverWait(driver, 15)  # Increased wait time
try:
    table = wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
    
    # Scroll down to ensure all data is loaded
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Wait for content to load

    # Extract headers
    headers = [th.text.strip() for th in table.find_elements(By.TAG_NAME, "th")]

    # Extract rows
    data = []
    rows = table.find_elements(By.TAG_NAME, "tr")
    for row in rows[1:]:  # Skip header row
        columns = row.find_elements(By.TAG_NAME, "td")
        if columns:
            data.append([col.text.strip() for col in columns])

    # Save to CSV
    csv_file = "scraped_data.csv"
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(data)

    print(f"Data saved to {csv_file}")

except Exception as e:
    print("Error:", e)

# Close the browser
driver.quit()
