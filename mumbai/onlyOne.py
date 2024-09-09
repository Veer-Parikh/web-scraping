from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Initialize the WebDriver
driver = webdriver.Chrome()

# Function to scrape data from a single page
def scrape_page_data(driver, url):
    driver.get(url)
    time.sleep(2)  # Wait for the page to load

    data = []
    try:
        # Find the main container
        main_container = driver.find_element(By.CLASS_NAME, "col-md-9.fullShow.col-lg-12")
        
        # Find all rows within the container
        row_elements = main_container.find_elements(By.CLASS_NAME, "row.shadow.p-3.mb-5.bg-body.rounded")

        for row in row_elements:
            try:
                # First Column: col-xl-4 (RERA number, project name, company, location)
                col_1 = row.find_element(By.CLASS_NAME, "col-xl-4")
                rera_number = col_1.find_element(By.TAG_NAME, "p").text.strip()
                project_name = col_1.find_element(By.CLASS_NAME, "title4").text.strip()
                company = col_1.find_elements(By.TAG_NAME, "p")[1].text.strip()
                location = col_1.find_element(By.CLASS_NAME, "fa-location-dot").find_element(By.XPATH, "..").text.strip()

                # Second Column: col-xl-6 (State, Pincode, District)
                col_2 = row.find_element(By.CLASS_NAME, "col-xl-6")
                state = col_2.find_elements(By.TAG_NAME, "p")[0].text.strip()
                pincode = col_2.find_elements(By.TAG_NAME, "p")[1].text.strip()
                district = col_2.find_elements(By.TAG_NAME, "p")[2].text.strip()

                # Only append the data if the district is "Mumbai Suburban"
                if district == "Mumbai Suburban":
                    data.append({
                        "RERA Number": rera_number,
                        "Project Name": project_name,
                        "Company": company,
                        "Location": location,
                        "District": district,
                        "State": state,
                        "Pincode": pincode
                    })

            except Exception as e:
                print(f"Error while processing row: {e}")
    
    except Exception as e:
        print(f"Error while processing page: {e}")
    
    return data

# Main function to loop through multiple pages
def scrape_multiple_pages(driver, base_url, max_pages):
    all_data = []
    for page in range(1, max_pages + 1):
        url = base_url + str(page)
        print(f"Scraping page {page}: {url}")
        page_data = scrape_page_data(driver, url)
        all_data.extend(page_data)
        time.sleep(1)  # Adjust sleep as necessary
    return all_data

# Set base URL (with page variable)
base_url = "https://maharera.maharashtra.gov.in/projects-search-result?project_name=&project_location=&project_completion_date=&project_state=27&project_district=Array&carpetAreas=&completionPercentages=&project_division=Array&page="

# Scrape up to 5 pages
max_pages = 5
all_scraped_data = scrape_multiple_pages(driver, base_url, max_pages)

# Save data to CSV (only projects from "Mumbai Suburban")
df = pd.DataFrame(all_scraped_data)
df.to_csv("maharera_projects_mumbai_suburban.csv", index=False)

# Close the browser
driver.quit()

print("Scraping complete. Data saved to maharera_projects_mumbai_suburban.csv")
