import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_data(driver, url):
    """
    Scrape data from a given URL.
    """
    try:
        driver.get(url)

        # Wait for the specific heading to appear
        heading = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//h3[text()='ARCHITECT']"))
        )

        # Find the table after the heading
        table = heading.find_element(By.XPATH, "following-sibling::table[1]")

        # Extract rows from the table
        rows = table.find_elements(By.XPATH, ".//tr")

        # Parse the table content
        data = []
        for row in rows:
            columns = row.find_elements(By.XPATH, ".//td")
            if columns:
                email = columns[0].text
                name = columns[1].text
                address = columns[2].text
                contact = columns[3].text
                data.append({
                    "Email Address": email,
                    "Name": name,
                    "Contact Address": address,
                    "Contact Number": contact
                })
        return data

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

# File paths
input_csv_file = "rera_project_data_final.csv"  # Replace with your input CSV file
output_csv_file = "output.csv"  # Replace with your desired output CSV file

# Selenium setup
driver = webdriver.Chrome()  # Adjust if using a different browser

try:
    # Read the input CSV and extract URLs
    with open(input_csv_file, mode="r", newline='', encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        urls = [row["level_2_href"] for row in reader]

    # Limit scraping to the first 10 URLs
    # urls = urls[:10]

    # Prepare to write the output CSV
    with open(output_csv_file, mode="w", newline='', encoding="utf-8") as outfile:
        fieldnames = ["URL", "Email Address", "Name", "Contact Address", "Contact Number"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        # Scrape data for each URL
        for i, url in enumerate(urls, start=1):
            print(f"Scraping {i}/{len(urls)}: {url}")
            scraped_data = scrape_data(driver, url)

            # Write scraped data to the output CSV
            if scraped_data:
                for record in scraped_data:
                    record["URL"] = url
                    writer.writerow(record)

finally:
    driver.quit()
