from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

# Initialize the WebDriver
driver = webdriver.Chrome()

def get_hrefs_from_page(driver):
    """Scrape hrefs from the current page."""
    hrefs = []
    try:
        # Locate the main container
        main_container = driver.find_element(By.CLASS_NAME, "col-md-9.fullShow.col-lg-12")

        # Find all elements within the container with the specified class
        row_elements = main_container.find_elements(By.CLASS_NAME, "row.shadow.p-3.mb-5.bg-body.rounded")

        # Iterate through each row element
        for row in row_elements:
            try:
                # Find the section within the row with the class name 'col-xl-2 divider'
                section = row.find_element(By.CLASS_NAME, "col-xl-2.divider")

                # Find the 'a' tag within the section with the class name 'listingList'
                listing_list = section.find_element(By.CLASS_NAME, "listingList")

                # Find the 'a' tag within the listing list and get its href attribute
                a_tag = listing_list.find_element(By.TAG_NAME, "a")
                href = a_tag.get_attribute("href")

                # Append the href to the list
                hrefs.append(href)
            except Exception as e:
                print(f"Error while processing row: {e}")
    except Exception as e:
        print(f"Error while processing page: {e}")
    
    return hrefs

def check_for_x_panel(driver, url):
    """Check if x_panel element exists in the given URL."""
    driver.get(url)
    time.sleep(5)  # Wait for the page to load
    
    try:
        promoter = driver.find_element(By.ID, "DivCoPromoter")
        x_panel = promoter.find_element(By.CLASS_NAME, "x_panel")
        if x_panel:
            return True
    except:
        return False

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
        view_details_table = driver.find_element(By.ID,"tblCoPromoter")
        co_promoter_name = view_details_table.find_element(By.ID, "CoPromoterName").get_attribute("value")
        block_name = view_details_table.find_element(By.ID,"CoPromoterHouseNo").get_attribute("value")
        locality = view_details_table.find_element(By.ID,"CoPromoterLocality").get_attribute("value")
        state = view_details_table.find_element(By.ID,"CoPromoterState").get_attribute("value")
        pincode = view_details_table.find_element(By.ID,"CoPromoterPincode").get_attribute("value")
        contact_name = view_details_table.find_element(By.ID,"CoPromoterContactName").get_attribute("value")
        contact_mobile = view_details_table.find_element(By.ID,"CoPromoterMobileNo").get_attribute("value")
        contact_office = view_details_table.find_element(By.ID,"CoPromoterOfficeNo").get_attribute("value")
        return co_promoter_name,block_name,locality,state,pincode,contact_mobile,contact_office,contact_name

    except Exception as e:
        print(f"Error processing {url}: {e}")
        return None

try:
    base_url = "https://maharera.maharashtra.gov.in/projects-search-result?project_name=&project_location=&project_completion_date=&project_state=27&project_district=0&carpetAreas=&completionPercentages=&project_division=&page="
    max_pages = 5  # Define a safety limit for the maximum number of pages to scrape
    current_page = 1
    all_data = []

    while current_page <= max_pages:
        # Navigate to the URL for the current page
        url = base_url + str(current_page)
        driver.get(url)
        time.sleep(5)  # Wait for the page to load

        # Get hrefs from the current page
        hrefs = get_hrefs_from_page(driver)
        print(f"Total hrefs collected on page {current_page}: {len(hrefs)}")

        # Process each href to check for x_panel and scrape data
        for href in hrefs:
            if check_for_x_panel(driver, href):
                co_promoter_name,block_name,locality,state,pincode,contact_mobile,contact_office,contact_name = process_href(driver, href)
                if co_promoter_name:
                    all_data.append({"CoPromoterName": co_promoter_name,"Block Name":block_name,"Locality":locality,"State":state,"Pincode":pincode,"Mobile":contact_mobile,"Office":contact_office,"Contact Name":contact_name})
                    print(f"Processed {href}: {co_promoter_name}")
            else:
                print(f"x_panel not found in: {href}")

            time.sleep(2)  # Adjust sleep duration as needed

        # Increment the current page count to move to the next page
        current_page += 1

    # Save the results to a CSV file
    df_results = pd.DataFrame(all_data)
    df_results.to_csv("co_promoter_names.csv", index=False)
    print("Processing complete. Results saved to co_promoter_names.csv.")

finally:
    # Quit the driver
    driver.quit()
