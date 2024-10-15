import logging
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Start the WebDriver
logging.info("Starting the WebDriver...")
driver = webdriver.Chrome()

# Open the provided Google Maps URL
logging.info("Opening Google Maps URL...")
driver.get("https://www.google.com/maps/search/cafes+in+mumbai/@19.1326479,72.9251802,10z/data=!3m1!4b1?entry=ttu&g_ep=EgoyMDI0MTAwOS4wIKXMDSoASAFQAw%3D%3D")

# Wait for the page to fully load
logging.info("Waiting for the page to load...")
time.sleep(10)

# Try to locate the scrollable div based on the updated classes
try:
    scrollable_div = driver.find_element(By.XPATH, "//div[@aria-label='Results for cafes in mumbai']")
    logging.info("Successfully located the scrollable div.")
except Exception as e:
    logging.error("Failed to locate the scrollable div: %s", e)
    driver.quit()

# Set up an ActionChains instance
actions = ActionChains(driver)

# Define a function to scroll and load more results
def scroll_down(scrollable_element, pause_time=1, max_scrolls=10):
    scrolls = 0
    previous_height = 0
    logging.info("Starting to scroll the results...")

    while scrolls < max_scrolls:
        try:
            # Scroll the div down
            actions.move_to_element(scrollable_element).perform()
            scrollable_element.send_keys(" ")
            logging.info(f"Scrolling iteration {scrolls + 1}...")
            
            # Wait for more results to load
            time.sleep(pause_time)
            # Check the scroll height to ensure new content is loading
            current_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_element)
            scrolls += 1
        except Exception as e:
            logging.error("Error during scrolling: %s", e)
            break

# Scroll down the div to load more results
scroll_down(scrollable_div)

# List to hold the scraped cafe data
cafes_data = []

# Try to extract cafe data
logging.info("Extracting cafe data...")

cafes = driver.find_elements(By.CLASS_NAME, "Nv2PK.THOPZb.CpccDe")

if cafes:
    logging.info(f"Found {len(cafes)} cafes.")
    for cafe in cafes:
        try:
            # Extract the cafe link
            link_element = cafe.find_element(By.CLASS_NAME, "hfpxzc")
            link = link_element.get_attribute('href')

            # Extract the div with all the data
            data_div = cafe.find_element(By.CLASS_NAME, "bfdHYd.Ppzolf.OFBs3e")

            # Extract specific data points
            cafe_name = data_div.find_element(By.CLASS_NAME, "qBF1Pd").text
            rating = data_div.find_element(By.CLASS_NAME, "MW4etd").text
            num_reviews = data_div.find_element(By.CLASS_NAME, "UY7F9").text
            price = data_div.find_element(By.CLASS_NAME, "HTCGSb").text
            category = data_div.find_element(By.CLASS_NAME, "W4Efsd").text
            address = data_div.find_element(By.XPATH, "//div[@class='W4Efsd'][2]").text  # Assuming this div contains the address

            # Append the data to the list
            cafes_data.append({
                "Cafe Name": cafe_name,
                "Rating": rating,
                "Number of Reviews": num_reviews,
                "Price Level": price,
                "Category": category,
                "Address": address,
                "Link": link
            })

        except Exception as e:
            logging.error("Error extracting data from a cafe: %s", e)
else:
    logging.error("No cafes found.")

# Convert the list of dictionaries into a pandas DataFrame
cafes_df = pd.DataFrame(cafes_data)

# Save the DataFrame to a CSV file
csv_filename = "cafes_in_mumbai.csv"
cafes_df.to_csv(csv_filename, index=False)
logging.info(f"Data saved to {csv_filename}")

# Close the browser after extraction
logging.info("Closing the WebDriver...")
driver.quit()
