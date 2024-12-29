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
    driver.get("https://rera.rajasthan.gov.in/ProjectSearch?Out=Y")  # Replace with the actual URL
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

    # Step 4: Collect project name, promoter name, and their "View" links (Level 1 Links)
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

    # Step 5: Visit each Level 1 link and find inner links (Level 2 Links)
    for project in project_details:
        driver.get(project["href"])
        time.sleep(3)  # Wait for the page to load

        # Locate nested links (Level 2 Links)
        nested_links = driver.find_elements(By.XPATH, '//tr[td[contains(text(), "Updated project details as on (12/26/2024)")]]//a[@title="View Details"]')
        level_2_links = [link.get_attribute('href') for link in nested_links]

        # Step 6: Visit each Level 2 link and scrape detailed data
        for href in level_2_links:
            driver.get(href)
            time.sleep(3)  # Wait for the page to load

            # Scrape Organization Name and Type
            try:
                organization_table = driver.find_element(By.XPATH, '//table[contains(@class, "table-bordered") and .//th[contains(text(), "Organization")]]')
                org_name = get_text_or_empty(organization_table.find_element(By.XPATH, './/td[contains(text(), "Organization Name")]/following-sibling::td'))
                org_type = get_text_or_empty(organization_table.find_element(By.XPATH, './/td[contains(text(), "Organization Type")]/following-sibling::td'))
            except:
                org_name, org_type = "", ""

            # Scrape Organization Contact Details
            try:
                contact_table = driver.find_element(By.XPATH, '//table[contains(@class, "table-bordered") and .//th[contains(text(), "Organization Contact Details")]]')
                office_number = get_text_or_empty(contact_table.find_element(By.XPATH, './/td[contains(text(), "Office Number")]/following-sibling::td'))
                website_url = get_text_or_empty(contact_table.find_element(By.XPATH, './/td[contains(text(), "Website URL")]/following-sibling::td'))
            except:
                office_number, website_url = "", ""

            # Scrape Land Details
            try:
                land_table = driver.find_element(By.XPATH, '//table[contains(@class, "table-bordered") and .//th[contains(text(), "Land Details")]]')
                plot_no = get_text_or_empty(land_table.find_element(By.XPATH, './/td[contains(text(), "Plot No. / Khasra No.")]/following-sibling::td'))
                total_area = get_text_or_empty(land_table.find_element(By.XPATH, './/td[contains(text(), "Total Area Of Project")]/following-sibling::td'))
                phase_area = get_text_or_empty(land_table.find_element(By.XPATH, './/td[contains(text(), "Phase Area")]/following-sibling::td'))
                fees = get_text_or_empty(land_table.find_element(By.XPATH, './/td[contains(text(), "Fees to be paid")]/following-sibling::td'))
                open_area = get_text_or_empty(land_table.find_element(By.XPATH, './/td[contains(text(), "Open Area")]/following-sibling::td'))
                num_apartments = get_text_or_empty(land_table.find_element(By.XPATH, './/td[contains(text(), "Number Of Apartments / Plots")]/following-sibling::td'))
                proposed_apartments = get_text_or_empty(land_table.find_element(By.XPATH, './/td[contains(text(), "Proposed But Not Sanctioned")]/following-sibling::td'))
                sanctioned_apartments = get_text_or_empty(land_table.find_element(By.XPATH, './/td[contains(text(), "Sanctioned Number")]/following-sibling::td'))
            except:
                plot_no, total_area, phase_area, fees, open_area, num_apartments, proposed_apartments, sanctioned_apartments = "", "", "", "", "", "", "", ""
            try:
                bank_table = driver.find_element(By.XPATH, '//table[contains(@class, "table-bordered") and .//td[contains(text(), "Bank Name")]]')
                bank_name = get_text_or_empty(bank_table.find_element(By.XPATH, './/td[contains(text(), "Bank Name")]/following-sibling::td'))
                branch_name = get_text_or_empty(bank_table.find_element(By.XPATH, './/td[contains(text(), "Branch Name")]/following-sibling::td'))
                account_number = get_text_or_empty(bank_table.find_element(By.XPATH, './/td[contains(text(), "Bank A/C Number")]/following-sibling::td'))
                account_holder = get_text_or_empty(bank_table.find_element(By.XPATH, './/td[contains(text(), "Name Of Bank Account Holder")]/following-sibling::td'))
            except:
                bank_name, branch_name, account_number, account_holder = "", "", "", ""

            # Scrape Cost Details
            # Scrape Cost Details
            try:
                cost_table = driver.find_element(By.XPATH, '//table[contains(@class, "table-bordered") and .//th[contains(text(), "Particular")]]')
                
                # Locate the specific rows for "Land cost" and "Development cost"
                land_cost = get_text_or_empty(cost_table.find_element(By.XPATH, './/tr[td/span[contains(text(), "Land cost as per rule 5(1)")]]/td[last()]'))
                development_cost = get_text_or_empty(cost_table.find_element(By.XPATH, './/tr[td/span[contains(text(), "Development cost as per rule 5(2)")]]/td[last()]'))
            except Exception as e:
                print(f"Error scraping cost details: {e}")
                land_cost, development_cost = "", ""

            # Append the scraped data
            scraped_data.append({
                "project_name": project["project_name"],
                "promoter_name": project["promoter_name"],
                "organization_name": org_name,
                "organization_type": org_type,
                "office_number": office_number,
                "website_url": website_url,
                "plot_no": plot_no,
                "total_area": total_area,
                "phase_area": phase_area,
                "fees_to_rera": fees,
                "open_area": open_area,
                "num_apartments": num_apartments,
                "proposed_apartments": proposed_apartments,
                "sanctioned_apartments": sanctioned_apartments,
                "bank_name": bank_name,
                "branch_name": branch_name,
                "account_number": account_number,
                "account_holder": account_holder,
                "land_cost": land_cost,
                "development_cost": development_cost
            })

    # Print the scraped data
    for data in scraped_data:
        print(data)

finally:
    # Close the WebDriver
    driver.quit()
