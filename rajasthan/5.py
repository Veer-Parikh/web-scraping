from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

# Initialize the WebDriver
driver = webdriver.Chrome()

# Function to extract text safely
def get_text_or_empty(element):
    try:
        return element.text.strip()
    except:
        return ""

# Data storage
scraped_data = []

try:
    driver.maximize_window()

    # Step 1: Navigate to the website
    driver.get("https://rera.rajasthan.gov.in/ProjectSearch?Out=Y")
    time.sleep(2)

    # Step 2: Select "Jaipur" from the dropdown
    district_dropdown = driver.find_element(By.ID, "DistrictId")
    select = Select(district_dropdown)
    select.select_by_visible_text("Jaipur")
    time.sleep(1)

    # Step 3: Click the "Search" button
    search_button = driver.find_element(By.ID, "btn_SearchProjectSubmit")
    search_button.click()
    time.sleep(5)  # Wait for the search results to load

    # Step 4: Scrape data from the search results table
    rows = driver.find_elements(By.XPATH, '//tr[@data-lvl="1"]')  # Locate table rows with project data
    project_details = []  # Store basic project details (name, promoter, and link)

    for row in rows[:10]:  # Limit to the first 10 rows
        try:
            project_name = get_text_or_empty(row.find_element(By.XPATH, './td[2]'))  # Project Name
            promoter_name = get_text_or_empty(row.find_element(By.XPATH, './td[4]'))  # Promoter Name
            view_link = row.find_element(By.XPATH, './/a[@title="View Details"]').get_attribute('href')  # "View" Link
            project_details.append({"project_name": project_name, "promoter_name": promoter_name, "href": view_link})
        except Exception as e:
            print(f"Error scraping table row: {e}")

    # Step 5: Visit each "View" link for deeper details
    for project in project_details:
        driver.get(project["href"])
        time.sleep(3)  # Wait for the page to load

        # Scrape organization details
        try:
            organization_table = driver.find_element(By.XPATH, '//table[contains(@class, "table-bordered") and .//th[contains(text(), "Organization")]]')
            org_name = get_text_or_empty(organization_table.find_element(By.XPATH, './/td[contains(text(), "Organization Name")]/following-sibling::td'))
            org_type = get_text_or_empty(organization_table.find_element(By.XPATH, './/td[contains(text(), "Organization Type")]/following-sibling::td'))
        except:
            org_name, org_type = "", ""

        # Scrape land details
        try:
            land_table = driver.find_element(By.XPATH, '//table[contains(@class, "table-bordered") and .//th[contains(text(), "Land Details")]]')
            plot_no = get_text_or_empty(land_table.find_element(By.XPATH, './/td[contains(text(), "Plot No. / Khasra No.")]/following-sibling::td'))
            total_area = get_text_or_empty(land_table.find_element(By.XPATH, './/td[contains(text(), "Total Area Of Project")]/following-sibling::td'))
        except:
            plot_no, total_area = "", ""

        # Combine data
        scraped_data.append({
            "project_name": project["project_name"],
            "promoter_name": project["promoter_name"],
            "organization_name": org_name,
            "organization_type": org_type,
            "plot_no": plot_no,
            "total_area": total_area,
        })

    # Print the final scraped data
    for data in scraped_data:
        print(data)

finally:
    # Close the WebDriver
    driver.quit()
