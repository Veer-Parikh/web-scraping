from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

# Initialize the WebDriver
driver = webdriver.Chrome()

def check_for_x_panel(driver, url):
    """Check if x_panel element exists in the given URL."""
    driver.get(url)
    time.sleep(5)  # Wait for the page to load
    
    try:
        promoter = driver.find_element(By.ID,"DivCoPromoter")
        x_panel = promoter.find_element(By.CLASS_NAME, "x_panel")
        if x_panel:
            return True
    except:
        return False

try:
    # Load hrefs from CSV file
    df = pd.read_csv("hrefs.csv")
    hrefs = df["Href"].tolist()

    hrefs_with_x_panel = []
    hrefs_without_x_panel = []

    for href in hrefs:
        if check_for_x_panel(driver, href):
            hrefs_with_x_panel.append(href)
            print(f"x_panel found in: {href}")
        else:
            hrefs_without_x_panel.append(href)

        time.sleep(2)  # Adjust sleep duration as needed

    # Save hrefs to separate CSV files
    df_with_x_panel = pd.DataFrame(hrefs_with_x_panel, columns=["Href"])
    df_with_x_panel.to_csv("hrefs_with_x_panel.csv", index=False)

    df_without_x_panel = pd.DataFrame(hrefs_without_x_panel, columns=["Href"])
    df_without_x_panel.to_csv("hrefs_without_x_panel.csv", index=False)

    print("Hrefs categorized and saved to separate files.")

finally:
    # Quit the driver
    driver.quit()
