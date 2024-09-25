from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

def scrape_bengaluru_urban_page(url):
    # Initialize the WebDriver (e.g., Chrome)
    driver = webdriver.Chrome()
    try:
        # Open the website
        driver.get(url)

        # Allow the page to load completely
        time.sleep(5)  # Adjust if necessary

        # Find the District dropdown by its ID and select "Bengaluru Urban"
        district_dropdown = Select(driver.find_element(By.ID, 'projectDist'))
        district_dropdown.select_by_visible_text('Bengaluru Urban')

        # Allow some time after selecting the district
        time.sleep(2)

        # Find the search button by its name and click it to submit the form
        search_button = driver.find_element(By.NAME, 'btn1')
        search_button.click()

        # Wait for the results page to load
        time.sleep(5)

        # Save the HTML content to a file (Optional)
        html_content = driver.page_source
        with open('bengaluru_urban_results.html', 'w', encoding='utf-8') as file:
            file.write(html_content)
        print("HTML content of the Bengaluru Urban page has been saved to 'bengaluru_urban_results.html'")

        # Locate and click the button to export the data as a PDF
        pdf_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Export Into PDF')]")
        pdf_button.click()

        # Wait for the download to complete
        time.sleep(5)  # Adjust this based on your download speed

        # Locate and click the button to export the data as an Excel file
        excel_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Export Into Excel')]")
        excel_button.click()

        # Wait for the download to complete
        time.sleep(5)  # Adjust this based on your download speed

    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Close the WebDriver
        driver.quit()

# Example usage
url = 'https://rera.karnataka.gov.in/projectViewDetails'  # Replace with the actual URL
scrape_bengaluru_urban_page(url)
