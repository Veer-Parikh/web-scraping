import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up WebDriver options
chrome_options = Options()
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--ignore-ssl-errors")
driver = webdriver.Chrome(options=chrome_options)

try:
    # Open the URL
    url = "https://www.gujrera.gujarat.gov.in"  # Replace with the actual URL
    driver.get(url)

    # 1. Wait for and click the first link
    first_link = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(
            (By.XPATH, "//div[@id='DataFromJson']//a[@class='figur underlineData' and contains(text(), '14,676')]")
        )
    )
    driver.execute_script("arguments[0].click();", first_link)
    print("Clicked on the first link (14,676).")

    # 2. Wait for and click the second link
    second_link = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(
            (By.XPATH, "//td//a[contains(@href, 'javascript:void(0);')]/strong[text()='14,675']")
        )
    )
    driver.execute_script("arguments[0].click();", second_link)
    print("Clicked on the second link (14,675).")

    # 3. Wait for the table to load
    table_body = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//tbody"))
    )

    # 4. Scrape data from all rows in the table
    rows = table_body.find_elements(By.TAG_NAME, "tr")
    data = []

    for row in rows:
        # Extract all cells in the row
        cells = row.find_elements(By.TAG_NAME, "td")
        row_data = [cell.text.strip() for cell in cells]
        data.append(row_data)

    # 5. Save data to a CSV file
    with open("scraped_data.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # Write header
        writer.writerow([
            "Sr. No.", "Market Name", "Enterprise Name", "Address", "Type",
            "Email", "Phone", "Link", "City", "Start Date", "End Date", "Status"
        ])
        # Write rows
        writer.writerows(data)

    print("Data saved to scraped_data.csv.")

except Exception as e:
    print(f"Error: {e}")
    driver.save_screenshot("error_debug.png")
finally:
    driver.quit()
