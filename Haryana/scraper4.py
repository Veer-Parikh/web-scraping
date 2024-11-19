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
        "Land Area": None,
        "Total Licensed Area": None,
        "Estimated Project Cost": None,
        "Cost of Land": None,
        "Cost of Construction": None,
        "Cost of Infrastructure": None,
        "Other Costs": None,
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
    
    # Part B Fields
    try:
        part_b = driver.find_element(By.ID, "part_b")
        land_area_element = part_b.find_element(By.XPATH, ".//label[contains(text(),'Land area of the project')]/../following-sibling::td/b")
        data["Land Area"] = land_area_element.text
    except Exception as e:
        print(f"Land Area not found in Part B on {url}. Error: {e}")

    try:
        licensed_area_element = part_b.find_element(By.XPATH, ".//label[contains(text(),'Total licensed area')]/../following-sibling::td/b")
        data["Total Licensed Area"] = licensed_area_element.text
    except Exception as e:
        print(f"Total Licensed Area not found in Part B on {url}. Error: {e}")
    
    # Part C Fields
    try:
        part_c = driver.find_element(By.ID, "part_c")
        project_cost_element = part_c.find_element(By.XPATH, ".//label[contains(text(),'Estimated cost of the project')]/../following-sibling::td/b")
        data["Estimated Project Cost"] = project_cost_element.text
    except Exception as e:
        print(f"Estimated Project Cost not found in Part C on {url}. Error: {e}")

    try:
        land_cost_element = part_c.find_element(By.XPATH, ".//label[contains(text(),'Cost of the land')]/../following-sibling::td/b")
        data["Cost of Land"] = land_cost_element.text
    except Exception as e:
        print(f"Cost of Land not found in Part C on {url}. Error: {e}")
    
    try:
        construction_cost_element = part_c.find_element(By.XPATH, ".//label[contains(text(),'Estimated cost of construction')]/../following-sibling::td/b")
        data["Cost of Construction"] = construction_cost_element.text
    except Exception as e:
        print(f"Cost of Construction not found in Part C on {url}. Error: {e}")
    
    try:
        infra_cost_element = part_c.find_element(By.XPATH, ".//label[contains(text(),'Estimated cost of infrastructure')]/../following-sibling::td/b")
        data["Cost of Infrastructure"] = infra_cost_element.text
    except Exception as e:
        print(f"Cost of Infrastructure not found in Part C on {url}. Error: {e}")
    
    try:
        other_costs_element = part_c.find_element(By.XPATH, ".//label[contains(text(),'Other Costs')]/../following-sibling::td/b")
        data["Other Costs"] = other_costs_element.text
    except Exception as e:
        print(f"Other Costs not found in Part C on {url}. Error: {e}")
    
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
