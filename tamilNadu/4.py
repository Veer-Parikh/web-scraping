from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import time

# Load WebDriver
driver = webdriver.Chrome()

# Input CSV file containing promoter & project links
input_file = "final.csv"  # Update filename if needed
output_file = "scraped_promoters.csv"

# Read promoter links (first column only)
promoter_links = []
with open(input_file, "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader, None)  # Skip header row if exists
    for row in reader:
        if row and len(row) > 0:  # Skip empty rows
            promoter_links.append(row[0])  # First column (Promoter Details)

# Print extracted links for debugging
print("Extracted Promoter Links:", promoter_links)
# Open the output CSV for writing
with open(output_file, "w", newline="", encoding="utf-8") as file:
    fieldnames = ["Type", "Firm Name", "Email", "Mobile 1", "Mobile 2", "Landline", "PAN Card", "Company Registration No"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

    # Loop through each promoter link and scrape data
    for link in promoter_links:
        try:
            driver.get(link)
            time.sleep(2)  # Let the page load

            # Extract details
            data = {
                "Type": driver.find_element(By.XPATH, "XPATH_TO_TYPE").text,
                "Firm Name": driver.find_element(By.XPATH, "XPATH_TO_FIRM_NAME").text,
                "Email": driver.find_element(By.XPATH, "XPATH_TO_EMAIL").text,
                "Mobile 1": driver.find_element(By.XPATH, "XPATH_TO_MOBILE_1").text,
                "Mobile 2": driver.find_element(By.XPATH, "XPATH_TO_MOBILE_2").text,
                "Landline": driver.find_element(By.XPATH, "XPATH_TO_LANDLINE").text,
                "PAN Card": driver.find_element(By.XPATH, "XPATH_TO_PAN").text,
                "Company Registration No": driver.find_element(By.XPATH, "XPATH_TO_COMPANY_REG").text,
            }

            # Write to CSV
            writer.writerow(data)
            print(f"Scraped: {data['Firm Name']}")

        except Exception as e:
            print(f"Failed to scrape {link}: {e}")

# Close WebDriver
driver.quit()
print(f"Scraping completed. Results saved to {output_file}")
