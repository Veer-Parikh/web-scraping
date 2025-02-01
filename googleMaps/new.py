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

# Scroll down to load all results
def scroll_down(scrollable_element, pause_time=3, max_scrolls=50):
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

# Extracting Href Links
href_links = []
business_elements = driver.find_elements(By.CLASS_NAME, "Nv2PK")

logging.info(f"Found {len(business_elements)} business listings to extract links.")

for element in business_elements:
    try:
        link_element = element.find_element(By.TAG_NAME, "a")
        href = link_element.get_attribute("href")
        if href:
            href_links.append({"URL": href})
            logging.info(f"Extracted: {href}")
    except Exception as e:
        logging.error(f"Error extracting href: {e}")
        continue

# Save to CSV
df = pd.DataFrame(href_links)
df.to_csv("real_estate_links_mumbai.csv", index=False)
logging.info("Data saved to 'real_estate_links_mumbai.csv'.")

# Close the browser
driver.quit()
