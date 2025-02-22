import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# Load CSV File
csv_file = "try.csv"
df = pd.read_csv(csv_file)  # Ensure it's comma-separated

urls = df['url'].tolist()
# areas = df['area'].tolist()  # Keep area for reference

driver = webdriver.Chrome()

def scrape_google_maps(url):
    try:
        driver.get(url)
        time.sleep(2)  # Wait for dynamic content to load

        try:
            business_name = driver.find_element(By.XPATH, "//h1").text.strip()
        except:
            business_name = "N/A"

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

        try:
            address = driver.find_element(By.XPATH, "//button[contains(@class, 'CsEnBe')]").text.strip()
        except:
            address = "N/A"

        try:
            phone_element = driver.find_element(By.XPATH, "//a[contains(@href, 'tel:')]")
            phone_number = phone_element.get_attribute("href").replace("tel:", "").strip()
        except:
            phone_number = "N/A"

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

scraped_data = []

for url, area in zip(urls):
    print(f"Scraping: {url}")
    data = scrape_google_maps(url)
    if data:
        # data["Area"] = area  # Add area to the scraped data
        scraped_data.append(data)
    time.sleep(2)

output_file = "scraped_business_data_new1.csv"
pd.DataFrame(scraped_data).to_csv(output_file, index=False)

print(f"Scraping complete! Data saved to {output_file}")

driver.quit()
