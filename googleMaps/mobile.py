import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load CSV File
csv_file = "TRY.csv"
df = pd.read_csv(csv_file, sep="\t")  # Adjust separator if needed

urls = df['URL'].tolist()

# Start WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode (no UI)
driver = webdriver.Chrome(options=options)

def scrape_google_maps(url):
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 5)  # Wait for elements

        # Extract Phone Number (Filter Out Address)
        try:
            phone_number_element = wait.until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(text(), '+91') or contains(text(), '0')]"))
            )
            phone_number = phone_number_element.text.strip()
            if len(phone_number) < 10 or " " in phone_number[:3]:  # Avoid wrong data
                phone_number = "N/A"
        except:
            phone_number = "N/A"

        # Extract Website URL (Fix for Missing Buttons)
        try:
            website_element = wait.until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'http') and not(contains(@href, 'google'))]"))
            )
            website_url = website_element.get_attribute('href')
        except:
            website_url = "N/A"

        return {
            "Phone Number": phone_number,
            "Website": website_url,
        }

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

# Scraping Process
scraped_data = []

for url in urls:
    print(f"Scraping: {url}")
    data = scrape_google_maps(url)
    if data:
        scraped_data.append(data)
    time.sleep(2)  # Prevent blocking

# Save to CSV
output_file = "scraped_contacts_fixed.csv"
pd.DataFrame(scraped_data).to_csv(output_file, index=False)

print(f"Scraping complete! Data saved to {output_file}")

# Close the driver
driver.quit()
