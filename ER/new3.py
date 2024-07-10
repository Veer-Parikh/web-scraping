from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Initialize the WebDriver
driver = webdriver.Chrome()

def scrape_hrefs(driver):
    """Scrape hrefs from the current page and interact with specific elements on those pages."""
    hrefs = []
    try:
        # Wait briefly to ensure the page has loaded
        time.sleep(5)

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

                # Visit the href to interact with specific elements
                driver.get(href)
                time.sleep(5)  # Allow the page to load

                # Check for the existence of the specified element and interact with it
                try:
                    x_panel = driver.find_element(By.CLASS_NAME, "x_panel")
                    view_details_button = x_panel.find_element(By.XPATH, ".//a[@class='btn btn-xs btn-info' and contains(@onclick, 'CoPromoterDetails')]")
                    view_details_button.click()
                    time.sleep(2)  # Allow any actions to complete

                    # Print the href where the x_panel is found
                    print(f"x_panel found at: {href}")
                except Exception as e:
                    print(f"Specific element not found on page {href}: {e}")
                
                # Navigate back to the main page
                driver.back()
                time.sleep(5)  # Allow the main page to reload

            except Exception as e:
                print(f"Error while processing row: {e}")
    except Exception as e:
        print(f"Error while processing page: {e}")
    
    return hrefs

def click_next_button(driver):
    """Click the 'Next' button to go to the next page or navigate to the next page URL directly."""
    try:
        # Find the pagination container
        pagination_container = driver.find_element(By.CLASS_NAME, "pagination")

        # Find the "Next" button within the pagination container
        next_button = pagination_container.find_element(By.CLASS_NAME, "next")

        # Get the href attribute of the "Next" button
        next_href = next_button.get_attribute("href")
        
        if next_href:
            # If we have the href attribute, navigate directly to that URL
            driver.get(next_href)
            return True
        else:
            print("No 'Next' href found.")
            return False
    except Exception as e:
        print("No more pages or error encountered:", e)
        return False

try:
    # Navigate to the URL
    driver.get("https://maharera.maharashtra.gov.in/projects-search-result")

    all_hrefs = []
    max_pages = 50  # Define a safety limit for the maximum number of pages to scrape
    current_page = 1

    # Loop to collect hrefs and navigate through pagination
    while current_page <= max_pages:
        # Scrape hrefs from the current page
        current_hrefs = scrape_hrefs(driver)
        all_hrefs.extend(current_hrefs)

        # Print the count and hrefs of collected hrefs
        print(f"Total hrefs collected so far: {len(all_hrefs)}")
        for href in current_hrefs:
            print(href)

        # Click the "Next" button to load the next set of results
        if not click_next_button(driver):
            print(f"No more pages found. Stopping after {current_page} pages.")
            break

        # Allow some time for the next page to load
        time.sleep(5)

        # Increment the current page count
        current_page += 1

    # Print the final count of collected hrefs
    print(f"Final count of hrefs collected: {len(all_hrefs)}")

finally:
    # Pause briefly to see the result before quitting the driver
    time.sleep(5)  # Adjust the sleep duration as needed
    driver.quit()
