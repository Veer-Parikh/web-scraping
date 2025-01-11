from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import time

# Load the project links from the CSV file
links_df = pd.read_csv("project_links1.csv")
project_links = links_df["Link"].tolist()  # Limit to the first 10 links

# Chrome options for better performance
options = webdriver.ChromeOptions()
options.page_load_strategy = 'none'  # Start interacting without waiting for the full page to load

# Initialize the WebDriver
driver = webdriver.Chrome(options=options)

# Storage for scraped project details
projects_data = []

# Function to stop the page load manually
def stop_page_load():
    try:
        driver.execute_script("window.stop();")
    except Exception as e:
        print(f"Error stopping the page load: {e}")

# Loop through each project link
for index, link in enumerate(project_links):
    print(f"Navigating to link {index + 1}/{len(project_links)}: {link}")
    driver.get(link)  # Navigate to the project link

    # Wait for the necessary element to appear or a short time before forcing stop
    time.sleep(2)  # Provide a short delay for initial loading
    stop_page_load()  # Forcefully stop loading the page

    try:
        # Scrape required details
        project_name = driver.find_element(By.XPATH, "//div[b[text()='Project Name :']]/following-sibling::div").text
        reg_number = driver.find_element(By.XPATH, "//div[b[text()='Registration Number :']]/following-sibling::div").text.split()[0]
        project_type = driver.find_element(By.XPATH, "//div[b[text()='Project Type :']]/following-sibling::div").text
        contact_number = driver.find_element(By.XPATH, "//div[b[text()='Contact Number :']]/following-sibling::div").text
        contact_email = driver.find_element(By.XPATH, "//div[b[text()='Contact Email :']]/following-sibling::div").text
        cost_of_construction = driver.find_element(By.XPATH, "//div[b[contains(text(),'Estimated Cost of Construction')]]/following-sibling::div").text
        cost_of_land = driver.find_element(By.XPATH, "//div[b[contains(text(),'Estimated Cost of Land')]]/following-sibling::div").text

        # Store data in a dictionary
        project_data = {
            "Project Name": project_name,
            "Registration Number": reg_number,
            "Project Type": project_type,
            "Contact Number": contact_number,
            "Contact Email": contact_email,
            "Estimated Cost of Construction (in lacs)": cost_of_construction,
            "Estimated Cost of Land (in lacs)": cost_of_land,
        }
        projects_data.append(project_data)

        # Print progress
        print(f"Successfully scraped project {index + 1}: {project_name}")

    except Exception as e:
        # Log the page source for debugging if scraping fails
        with open(f"debug_page_{index + 1}.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print(f"Failed to scrape project at {link}: {e}")
        print(f"Page source saved to debug_page_{index + 1}.html")

# Save the scraped data to a CSV file
projects_df = pd.DataFrame(projects_data)
projects_df.to_csv("project_details1.csv", index=False)

# Close the browser
driver.quit()

# Print completion message
print("Scraping completed. Project details saved to 'project_details.csv'.")

# SHIVLOK GREENS (EXISTING INCOMPLETE PHASE-2),P-BPL-17-006,Ongoing,9826055819,draupadiconstruction@gmail.com,2624.26,2077.00
