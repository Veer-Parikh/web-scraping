from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, TimeoutException
import time

def get_driver():
    # Setup Chrome WebDriver options
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    return driver

def get_project_details(driver, url):
    driver.get(url)
    time.sleep(2)  # Allow time for page load

    # Extract promoter, CEO/MD details
    promoter_ceo_md_details = get_promoter_ceo_md_details(driver)
    
    # Switch to menu 4 (Bank details)
    bank_details = get_bank_details(driver)

    # Check if there are registered agents or insurance
    extra_details = check_registered_agents_and_insurance(driver)

    project_info = {
        'promoter_ceo_md_details': promoter_ceo_md_details,
        'bank_details': bank_details,
        'extra_details': extra_details,
    }

    return project_info

def get_promoter_ceo_md_details(driver):
    try:
        # Wait and locate the element for promoter, CEO/MD
        promoter_ceo_md_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='promoter_ceo_md']"))  # Modify the XPATH accordingly
        )
        promoter_ceo_md_details = promoter_ceo_md_element.text
        return promoter_ceo_md_details
    except (NoSuchElementException, TimeoutException):
        return "Details not found"
    except StaleElementReferenceException:
        return "Stale element reference error"

def get_bank_details(driver):
    try:
        # Locate and click the Menu 4 tab (Bank Details)
        menu4_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='menu4']"))  # Modify the XPATH accordingly
        )
        menu4_tab.click()
        time.sleep(2)  # Wait for the content to load

        # Locate and extract bank details
        bank_details_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='bank_details']"))  # Modify the XPATH accordingly
        )
        bank_details = bank_details_element.text
        return bank_details
    except (NoSuchElementException, TimeoutException):
        return "Bank details not found"
    except StaleElementReferenceException:
        return "Stale element reference error"

def check_registered_agents_and_insurance(driver):
    try:
        # Locate the registered agent field and insurance field
        registered_agent_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='registered_agents']"))  # Modify the XPATH accordingly
        )
        insurance_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='insurance']"))  # Modify the XPATH accordingly
        )

        registered_agents = registered_agent_element.text if 'NO' not in registered_agent_element.text else 'NO'
        insurance_done = insurance_element.text if 'NO' not in insurance_element.text else 'NO'

        return {'is there any registered agents for this projects?': registered_agents, 'is there any insurance done?': insurance_done}

    except (NoSuchElementException, TimeoutException):
        return {'is there any registered agents for this projects?': 'NO', 'is there any insurance done?': 'NO'}
    except StaleElementReferenceException:
        return {'error': 'Stale element reference error'}

if __name__ == "__main__":
    driver = get_driver()
    url = "https://example.com/project_page"  # Replace with actual project URL

    try:
        project_details = get_project_details(driver, url)
        print(project_details)
    finally:
        driver.quit()
                                                                                        