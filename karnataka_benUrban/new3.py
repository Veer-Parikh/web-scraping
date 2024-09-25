from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def search_by_application_number(url, application_number):
    # Initialize the WebDriver (e.g., Chrome)
    driver = webdriver.Chrome()

    try:
        # Open the website
        driver.get(url)

        # Allow the page to load completely
        time.sleep(5)  # Adjust if necessary

        # Find the Application Number input field by its ID and input the given application number
        app_no_input = driver.find_element(By.ID, 'regNo')
        app_no_input.send_keys(application_number)

        # Allow some time after inputting the data
        time.sleep(2)

        # Find the search button by its name and click it to submit the form
        search_button = driver.find_element(By.NAME, 'btn1')
        search_button.click()

        # Wait for the results page to load
        time.sleep(5)

        # Optionally, you can now scrape the resulting page or do other actions
        html_content = driver.page_source
        
        # Save the HTML content to a file
        with open('search_results.html', 'w', encoding='utf-8') as file:
            file.write(html_content)
        
        print("HTML content of the search results page has been saved to 'search_results.html'")
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Close the WebDriver
        driver.quit()

# Example usage
url = 'https://rera.karnataka.gov.in/projectViewDetails'  # Replace with the actual URL
application_number = 'ACK/KA/RERA/1251/310/PR/290724/008372'
search_by_application_number(url, application_number)
