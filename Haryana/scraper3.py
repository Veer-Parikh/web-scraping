from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Function to scrape data from each href
def scrape_details(url):
    driver.get(url)
    
    # Wait for the page to load (adjust the timeout as needed)
    wait = WebDriverWait(driver, 10)
    
    # Initialize a dictionary for storing the scraped data
    data = {
        "Phone": None,
        "Email": None,
        "Website": None,
        "CIN": None,
        "Name": [],
        "Residential Address": [],
        "Phone (Landline)": [],
        "Phone (Mobile)": [],
        "Email ID": [],
    }
    
    try:
        # Scrape Phone (Mobile)
        phone_element = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//label[text()='Phone(Mobile)']/../following-sibling::td/b")
        ))
        data["Phone"] = phone_element.text
    except Exception as e:
        print(f"Phone not found on {url}. Error: {e}")

    try:
        # Scrape Email ID
        email_element = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//label[text()='Email ID']/../following-sibling::td/b")
        ))
        data["Email"] = email_element.text
    except Exception as e:
        print(f"Email not found on {url}. Error: {e}")
    
    try:
        # Scrape Website
        website_element = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//label[text()='Website']/../following-sibling::td/b")
        ))
        data["Website"] = website_element.text
    except Exception as e:
        print(f"Website not found on {url}. Error: {e}")
    
    try:
        # Scrape CIN No.
        cin_element = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//label[contains(text(),'CIN No.')]/../following-sibling::td/b")
        ))
        data["CIN"] = cin_element.text
    except Exception as e:
        print(f"CIN not found on {url}. Error: {e}")

    # Additional fields (handling multiple occurrences)
    try:
        # Scrape all Names
        name_elements = driver.find_elements(By.XPATH, "//label[contains(text(),'Name')]/b")
        data["Name"] = [name.text for name in name_elements]
    except Exception as e:
        print(f"Names not found on {url}. Error: {e}")
    
    try:
        # Scrape all Residential Addresses
        address_elements = driver.find_elements(By.XPATH, "//label[contains(text(),'Residential Address')]/b")
        data["Residential Address"] = [address.text for address in address_elements]
    except Exception as e:
        print(f"Residential Addresses not found on {url}. Error: {e}")
    
    try:
        # Scrape all Phone (Landline) entries
        phone_landline_elements = driver.find_elements(By.XPATH, "//label[contains(text(),'Phone (landline)')]/b")
        data["Phone (Landline)"] = [landline.text for landline in phone_landline_elements]
    except Exception as e:
        print(f"Phone (Landline) entries not found on {url}. Error: {e}")
    
    try:
        # Scrape all Phone (Mobile) entries
        phone_mobile_elements = driver.find_elements(By.XPATH, "//label[contains(text(),'Phone (Mobile)')]/b")
        data["Phone (Mobile)"] = [mobile.text for mobile in phone_mobile_elements]
    except Exception as e:
        print(f"Phone (Mobile) entries not found on {url}. Error: {e}")
    
    try:
        # Scrape all Promoter Email IDs
        promoter_email_elements = driver.find_elements(By.XPATH, "//label[contains(text(),'Email ID')]/b")
        data["Email ID"] = [email.text for email in promoter_email_elements]
    except Exception as e:
        print(f"Promoter Email IDs not found on {url}. Error: {e}")

    return data

# Set up the WebDriver
driver = webdriver.Chrome()

# List of first 5 hrefs for testing
hrefs = [
    "https://haryanarera.gov.in/view_project/project_preview_open/1444",
    "https://haryanarera.gov.in/view_project/project_preview_open/1634"
]

# Loop through each href and scrape data
results = []
for href in hrefs:
    print(f"Scraping: {href}")
    scraped_data = scrape_details(href)
    results.append(scraped_data)
    print(scraped_data)  # Print the data for debugging

# Close the driver
driver.quit()

# Print all results
print("Final Results:")
for result in results:
    print(result)
