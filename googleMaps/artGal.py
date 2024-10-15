import logging
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Start the WebDriver
logging.info("Starting the WebDriver...")
driver = webdriver.Chrome()

# Open the provided Google Maps URL for art galleries
logging.info("Opening Google Maps URL for art galleries...")
driver.get("https://www.google.com/maps/search/art+galleries+in+mumbai/")  # Replace with the actual URL

# Wait for the page to fully load
logging.info("Waiting for the page to load...")
time.sleep(10)

# Scroll down to load all results (adjust as needed)
def scroll_down(scrollable_element, pause_time=1, max_scrolls=10):
    scrolls = 0
    logging.info("Starting to scroll the results for art galleries...")

    while scrolls < max_scrolls:
        try:
            # Scroll the div down
            scrollable_element.send_keys(" ")
            logging.info(f"Scrolling iteration {scrolls + 1}...")

            # Wait for more results to load
            time.sleep(pause_time)
            scrolls += 1
        except Exception as e:
            logging.error("Error during scrolling: %s", e)
            break

# Locate the scrollable div for art galleries
try:
    scrollable_div = driver.find_element(By.XPATH, "//div[@aria-label='Results for art galleries in mumbai']")
    logging.info("Successfully located the scrollable div for art galleries.")
    scroll_down(scrollable_div)
except Exception as e:
    logging.error("Failed to locate the scrollable div: %s", e)
    driver.quit()

# Scraping the data for each gallery
galleries = []

# Locate all gallery elements
gallery_elements = driver.find_elements(By.CLASS_NAME, "Nv2PK.THOPZb.CpccDe")

logging.info(f"Found {len(gallery_elements)} gallery elements to scrape.")

for element in gallery_elements:
    try:
        # Get the link (href) from the 'a' tag with class 'hfpxzc'
        link = element.find_element(By.CLASS_NAME, "hfpxzc").get_attribute("href")
        
        # Get the div that contains the data (class 'bfdHYd Ppzolf OFBs3e')
        data_div = element.find_element(By.CLASS_NAME, "bfdHYd.Ppzolf.OFBs3e")
        
        # Extract gallery name
        name = data_div.find_element(By.CLASS_NAME, "qBF1Pd.fontHeadlineSmall").text
        
        # Extract rating
        rating_div = data_div.find_element(By.CLASS_NAME, "e4rVHe.fontBodyMedium")
        rating = rating_div.find_element(By.CLASS_NAME, "MW4etd").text
        
        # Extract number of reviews
        reviews = rating_div.find_element(By.CLASS_NAME, "UY7F9").text
        
        # Extract type of place (e.g., Art Gallery)
        type_of_place = data_div.find_elements(By.CLASS_NAME, "W4Efsd")[1].text
        
        # Extract address
        address = data_div.find_elements(By.CLASS_NAME, "W4Efsd")[2].text
        
        # Extract opening status and time
        timings = data_div.find_elements(By.CLASS_NAME, "W4Efsd")[3].text

        # Append all details to the galleries list
        galleries.append({
            "Name": name,
            "Link": link,
            "Rating": rating,
            "Number of Reviews": reviews,
            "Type": type_of_place,
            "Address": address,
            "Timings": timings
        })
        
        logging.info(f"Scraped data for: {name}")

    except Exception as e:
        logging.error(f"Error scraping element: {e}")
        continue

# Save the scraped data to a CSV file
df = pd.DataFrame(galleries)
df.to_csv('art_galleries_mumbai.csv', index=False)
logging.info("Data saved to 'art_galleries_mumbai.csv'.")

# Close the browser
driver.quit()
