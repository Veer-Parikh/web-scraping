import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC

# Load CSV File
csv_file = "TRY.csv"
df = pd.read_csv(csv_file, sep="\t")  # If it's tab-separated

urls = df['URL'].tolist()

# Configure Selenium
# chrome_options = Options()
# chrome_options.add_argument("--headless")  # Run in headless mode (no browser UI)
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-dev-shm-usage")

# Start WebDriver
# service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome()

def scrape_google_maps(url):
    try:
        driver.get(url)
        time.sleep(2)  # Wait for dynamic content to load

        # Extract Business Name
        try:
            business_name = driver.find_element(By.XPATH, "//h1").text.strip()
        except:
            business_name = "N/A"

        # Extract Category
        try:
            category = driver.find_element(By.XPATH, "//button[contains(@class, 'DkEaL')]").text.strip()
        except:
            category = "N/A"

        try:
            rating = driver.find_element(By.XPATH, "//div[contains(@class, 'F7nice')]//span[@aria-hidden='true']").text.strip()
        except:
            rating = "N/A"

        try:
            num_reviews = driver.find_element(By.XPATH, "//span[contains(@aria-label, 'reviews')]").text.strip()
        except:
            num_reviews = "N/A"

        # Extract Address
        try:
            address = driver.find_element(By.XPATH, "//button[contains(@class, 'CsEnBe')]").text.strip()
        except:
            address = "N/A"

        # Extract Phone Number
# Extract Phone Number using the unique symbol
        try:
            phone_element = driver.find_element(By.XPATH, "//a[contains(@href, 'tel:')]")
            phone_number = phone_element.get_attribute("href").replace("tel:", "").strip()
        except:
            phone_number = "N/A"



        # Extract Operating Hours
        try:
            hours = driver.find_element(By.XPATH, "//div[contains(@class, 'OqCZI')]").text.strip()
        except:
            hours = "N/A"

        return {
            "Business Name": business_name,
            "Category": category,
            "Rating": rating,
            "Number of Reviews": num_reviews,
            "Phone Number": phone_number,
            "Address": address,
            "Operating Hours": hours,
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
    time.sleep(2)  # Avoid getting blocked

# Save to CSV
output_file = "scraped_business_data_new1.csv"
pd.DataFrame(scraped_data).to_csv(output_file, index=False)

print(f"Scraping complete! Data saved to {output_file}")

# Close the driver
driver.quit()
