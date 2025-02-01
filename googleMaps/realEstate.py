import logging
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Start WebDriver
logging.info("Starting the WebDriver...")
driver = webdriver.Chrome()

# Open Google Maps Search for Real Estate Agents in Mumbai
logging.info("Opening Google Maps search...")
driver.get("https://www.google.com/maps/search/real+estate+agents+in+mumbai/")

# Wait for the page to load
logging.info("Waiting for the page to load...")
time.sleep(10)

# Scroll down to load all results (adjust scroll count as needed)
def scroll_down(scrollable_element, pause_time=2, max_scrolls=15):
    scrolls = 0
    logging.info("Scrolling through search results...")

    while scrolls < max_scrolls:
        try:
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_element)
            time.sleep(pause_time)
            scrolls += 1
        except Exception as e:
            logging.error("Scrolling error: %s", e)
            break

# Locate the scrollable div
try:
    scrollable_div = driver.find_element(By.XPATH, "//div[contains(@aria-label, 'Results for')]")
    logging.info("Scrollable div located.")
    scroll_down(scrollable_div)
except Exception as e:
    logging.error("Failed to locate the scrollable div: %s", e)
    driver.quit()

# Scraping Data
agents = []

# Locate all business elements
business_elements = driver.find_elements(By.CLASS_NAME, "Nv2PK")

logging.info(f"Found {len(business_elements)} business listings to scrape.")

for element in business_elements:
    try:
        # Business Name
        name = element.find_element(By.CLASS_NAME, "qBF1Pd.fontHeadlineSmall").text
        
        # Rating (Stars)
        rating = element.find_element(By.CLASS_NAME, "MW4etd").text
        
        # Number of Reviews
        reviews = element.find_element(By.CLASS_NAME, "UY7F9").text
        
        # Mobile Number
        try:
            mobile_number = element.find_element(By.CLASS_NAME, "UsdlK").text
        except:
            mobile_number = "N/A"  # Some listings may not have a phone number
        
        # Website URL
        try:
            website_url = element.find_element(By.CSS_SELECTOR, "a[aria-label*='Visit']").get_attribute("href")
        except:
            website_url = "N/A"  # Some listings may not have a website
        
        # Append to list
        agents.append({
            "Name": name,
            "Rating": rating,
            "Number of Reviews": reviews,
            "Mobile Number": mobile_number,
            "Website": website_url,
        })

        logging.info(f"Scraped: {name}")

    except Exception as e:
        logging.error(f"Error scraping element: {e}")
        continue

# Save to CSV
df = pd.DataFrame(agents)
df.to_csv("real_estate_agents_mumbai.csv", index=False)
logging.info("Data saved to 'real_estate_agents_mumbai.csv'.")

# Close the browser
driver.quit()
