from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
driver = webdriver.Chrome()
from selenium.common.exceptions import NoSuchElementException

def scrape_directors_by_xpath(driver):
    try:
        # Use the XPath to find all director/partner name elements
        director_sections = driver.find_elements(By.XPATH, "//div[contains(@class, 'col-lg-8') and contains(@class, 'col-md-8') and contains(@class, 'col-sm-12') and contains(@class, 'col-xs-12')]")
        
        director_names = []
        for section in director_sections:
            if "Director / Partner Name :" in section.text:
                # Extract the relevant text
                director_names.append(section.text.replace("Director / Partner Name :", "").strip())
        return director_names
    except NoSuchElementException:
        print("Director / Partner information not found on this page.")
        return []

def scrape_promoter_by_xpath(driver):
    try:
        # Use the XPath to locate the promoter information
        promoter_section = driver.find_element(By.XPATH, "//label[contains(text(),'Promoter Detail')]")  # Update with the actual class for promoter
        promoter_name = promoter_section.text.strip()
        return promoter_name
    except NoSuchElementException:
        print("Promoter information not found on this page.")
        return None

# Example usage
driver.get("https://rera.tn.gov.in/public-view1/building/pfirm/7d309a20-8d3d-11ef-8b35-69430d6e07d6")
directors = scrape_directors_by_xpath(driver)
promoter = scrape_promoter_by_xpath(driver)

scraped_details = {
    "Directors": directors,
    "Promoter": promoter
}
print(scraped_details)
