from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

# Initialize the WebDriver
driver = webdriver.Chrome()

def process_href(driver, url):
    """Process each href to find and click on the necessary elements and extract data."""
    driver.get(url)
    time.sleep(5)  # Wait for the page to load
    
    try:
        # Locate the DivCoPromoter element by ID
        div_co_promoter = driver.find_element(By.ID, "DivCoPromoter")

        # Find the table within the DivCoPromoter
        table = div_co_promoter.find_element(By.CLASS_NAME, "table.table-bordered.table-responsive.table-striped")
        
        # Find the 'View Details' button and click it
        view_details_button = table.find_element(By.CLASS_NAME, "btn.btn-xs.btn-info")
        view_details_button.click()
        time.sleep(2)  # Wait for the details to load

        # Extract the value from the CoPromoterName input element
        co_promoter_name = driver.find_element(By.ID, "CoPromoterName").get_attribute("value")
        return co_promoter_name

    except Exception as e:
        print(f"Error processing {url}: {e}")
        return None

try:
    # Load hrefs from CSV file
    df = pd.read_csv("hrefs_with_x_panel.csv")
    hrefs = df["Href"].tolist()

    results = []

    for href in hrefs:
        co_promoter_name = process_href(driver, href)
        if co_promoter_name:
            results.append({"CoPromoterName": co_promoter_name})
            print(f"Processed {href}: {co_promoter_name}")

        time.sleep(2)  # Adjust sleep duration as needed

    # Save results to a CSV file
    df_results = pd.DataFrame(results)
    df_results.to_csv("co_promoter_names.csv", index=False)

    print("Processing complete. Results saved to co_promoter_names.csv.")

finally:
    # Quit the driver
    driver.quit()
