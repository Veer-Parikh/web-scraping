import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager

# Load CSV File
csv_file = "real_estate_links_mumbai.csv"
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
        time.sleep(5)  # Wait for dynamic content to load

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

        # Extract Rating
        try:
            rating = driver.find_element(By.XPATH, "//span[contains(@class, 'Aq14fc')]").text.strip()
        except:
            rating = "N/A"

        # Extract Number of Reviews
        try:
            num_reviews = driver.find_element(By.XPATH, "//span[contains(@class, 'AYi5wd')]").text.strip()
        except:
            num_reviews = "N/A"

        # Extract Address
        try:
            address = driver.find_element(By.XPATH, "//button[contains(@class, 'CsEnBe')]").text.strip()
        except:
            address = "N/A"

        # Extract Phone Number
        try:
            phone_number = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Phone')]").text.strip()
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
output_file = "scraped_business_data.csv"
pd.DataFrame(scraped_data).to_csv(output_file, index=False)

print(f"Scraping complete! Data saved to {output_file}")

# Close the driver
driver.quit()
