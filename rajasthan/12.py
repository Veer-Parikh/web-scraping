import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Helper function to safely extract text
def get_text_or_empty(element):
    try:
        return element.text.strip()
    except:
        return ""

# Initialize WebDriver
driver = webdriver.Chrome()

# Load Level 1 hrefs from CSV
hrefs_df = pd.read_csv("hrefs_level_1.csv")  # Adjust file path if necessary
level_1_hrefs = hrefs_df["href"].tolist()

# Store scraped data
scraped_data = []

try:
    for idx, href in enumerate(level_1_hrefs):
        if idx == 20:
            break
        print(f"Processing Level 1 link {idx + 1}/{len(level_1_hrefs)}: {href}")
        driver.get(href)
        time.sleep(3)  # Wait for the page to load

        # Locate nested Level 2 links
        try:
            nested_links = driver.find_elements(By.XPATH, '//tr[td[contains(text(), "Updated project details as on")]]//a[@title="View Details"]')
            level_2_links = [link.get_attribute('href') for link in nested_links]
        except Exception as e:
            print(f"No Level 2 links found on {href}: {e}")
            continue

        # Process each Level 2 link
        for level_2_href in level_2_links:
            print(f"Visiting Level 2 link: {level_2_href}")
            driver.get(level_2_href)
            time.sleep(3)  # Wait for the page to load

            # Scrape data
            try:
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

                # Scrape Bank Details
                try:
                    bank_table = driver.find_element(By.XPATH, '//table[contains(@class, "table-bordered") and .//td[contains(text(), "Bank Name")]]')
                    bank_name = get_text_or_empty(bank_table.find_element(By.XPATH, './/td[contains(text(), "Bank Name")]/following-sibling::td'))
                    branch_name = get_text_or_empty(bank_table.find_element(By.XPATH, './/td[contains(text(), "Branch Name")]/following-sibling::td'))
                    account_number = get_text_or_empty(bank_table.find_element(By.XPATH, './/td[contains(text(), "Bank A/C Number")]/following-sibling::td'))
                    account_holder = get_text_or_empty(bank_table.find_element(By.XPATH, './/td[contains(text(), "Name Of Bank Account Holder")]/following-sibling::td'))
                except:
                    bank_name, branch_name, account_number, account_holder = "", "", "", ""

                # Scrape Cost Details
                try:
                    cost_table = driver.find_element(By.XPATH, '//table[contains(@class, "table-bordered") and .//th[contains(text(), "Particular")]]')
                    land_cost = get_text_or_empty(cost_table.find_element(By.XPATH, './/tr[td/span[contains(text(), "Land cost as per rule 5(1)")]]/td[last()]'))
                    development_cost = get_text_or_empty(cost_table.find_element(By.XPATH, './/tr[td/span[contains(text(), "Development cost as per rule 5(2)")]]/td[last()]'))
                except:
                    land_cost, development_cost = "", ""

                # Append the scraped data
                scraped_data.append({
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
                    "development_cost": development_cost,
                    "level_2_href": level_2_href
                })
            except Exception as e:
                print(f"Error scraping Level 2 link {level_2_href}: {e}")

    # Save to CSV
    df = pd.DataFrame(scraped_data)
    df.to_csv("rera_project_data_final.csv", index=False)
    print("Data saved to rera_project_data.csv.")

finally:
    driver.quit()
