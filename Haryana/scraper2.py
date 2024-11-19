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
        "Name": None,
        "Residential Address": None,
        "Phone (Landline)": None,
        "Phone (Mobile)": None,
        "Email ID": None,
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

    # Additional fields
    try:
        # Scrape Name
        name_element = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//label[contains(text(),'Name')]/b")
        ))
        data["Name"] = name_element.text
    except Exception as e:
        print(f"Name not found on {url}. Error: {e}")
    
    try:
        # Scrape Residential Address
        address_element = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//label[contains(text(),'Residential Address')]/b")
        ))
        data["Residential Address"] = address_element.text
    except Exception as e:
        print(f"Residential Address not found on {url}. Error: {e}")
    
    try:
        # Scrape Phone (Landline)
        phone_landline_element = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//label[contains(text(),'Phone (landline)')]/b")
        ))
        data["Phone (Landline)"] = phone_landline_element.text
    except Exception as e:
        print(f"Phone (Landline) not found on {url}. Error: {e}")
    
    try:
        # Scrape Phone (Mobile) (updated for Promoter's Mobile Number)
        promoter_phone_element = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//label[contains(text(),'Phone (Mobile)')]/b")
        ))
        data["Phone (Mobile)"] = promoter_phone_element.text
    except Exception as e:
        print(f"Phone (Mobile) not found on {url}. Error: {e}")
    
    try:
        # Scrape Promoter Email ID
        promoter_email_element = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//label[contains(text(),'Email ID')]/b")
        ))
        data["Email ID"] = promoter_email_element.text
    except Exception as e:
        print(f"Email ID not found on {url}. Error: {e}")

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
