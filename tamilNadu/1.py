from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

# Initialize WebDriver
# options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # Run Chrome in headless mode for faster execution (remove this for debugging)
driver = webdriver.Chrome()

# URL to start with
start_url = "https://rera.tn.gov.in/registered-building/tn"

# Storage for scraped data
scraped_data = []

# Function to scrape href links from the current page
def scrape_page():
    try:
        # Find all the relevant <td> elements
        table_cells = driver.find_elements(By.XPATH, "//td[a[contains(text(),'Promoter Details')]]")

        for cell in table_cells:
            try:
                # Extract the "Promoter Details" href
                promoter_link = cell.find_element(By.XPATH, "./a[contains(text(),'Promoter Details')]").get_attribute("href")
                # Extract the "Project Details" href
                project_link = cell.find_element(By.XPATH, "./a[contains(text(),'Project Details')]").get_attribute("href")

                # Store the links in the list
                scraped_data.append({
                    "Promoter Details": promoter_link,
                    "Project Details": project_link,
                })
                print(f"Scraped: {promoter_link}, {project_link}")

            except Exception as e:
                print(f"Error scraping cell: {e}")

    except Exception as e:
        print(f"Error scraping page: {e}")

# Function to check if the "Next" button is enabled and click it
def go_to_next_page():
    try:
        next_button = driver.find_element(By.XPATH, "//a[@role='link' and @data-dt-idx='next']")
        if "disabled" not in next_button.get_attribute("class"):
            next_button.click()
            time.sleep(2)  # Short delay for the next page to load
            return True
        else:
            print("No more pages to scrape.")
            return False
    except Exception as e:
        print(f"Error finding the 'Next' button: {e}")
        return False

# Start scraping process
try:
    driver.get(start_url)
    time.sleep(3)  # Allow initial page to load

    while True:
        print("Scraping current page...")
        scrape_page()

        print("Attempting to go to the next page...")
        if not go_to_next_page():
            break

except Exception as e:
    print(f"Error during scraping process: {e}")

finally:
    # Save the scraped data to a CSV file
    df = pd.DataFrame(scraped_data)
    df.to_csv("scraped_links.csv", index=False)
    print("Scraping completed. Data saved to 'scraped_links.csv'.")

    # Close the browser
    driver.quit()
