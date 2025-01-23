import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Initialize WebDriver
driver = webdriver.Chrome()

# Define a function to extract text safely
def get_text_safe(element):
    return element.text.strip() if element else None

# Read the CSV file containing promoter links
promoter_links = []
with open("final.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        promoter_links.append(row["Promoter Details"])

# Initialize result storage
results = []

# Loop through each promoter link
for index, link in enumerate(promoter_links, start=1):
    print(f"Processing link {index}/{len(promoter_links)}: {link}")
    driver.get(link)
    time.sleep(3)  # Adjust delay based on page load speed

    # Scrape Promoter Details
    promoter_details = {}
    try:
        form_section = driver.find_element(By.CLASS_NAME, "l_forms")
        promoter_details["Type"] = get_text_safe(form_section.find_element(By.XPATH, ".//p1[text()='Type of Promoter :']/following-sibling::p"))
        promoter_details["Firm Name"] = get_text_safe(form_section.find_element(By.XPATH, ".//p1[text()='Firm Name :']/following-sibling::p"))
        promoter_details["Email"] = get_text_safe(form_section.find_element(By.XPATH, ".//p1[text()='Email ID :']/following-sibling::p"))
        promoter_details["Mobile 1"] = get_text_safe(form_section.find_element(By.XPATH, ".//p1[text()='Mobile No. 1 :']/following-sibling::p"))
        promoter_details["Mobile 2"] = get_text_safe(form_section.find_element(By.XPATH, ".//p1[text()='Mobile No. 2 :']/following-sibling::p"))
        promoter_details["Landline"] = get_text_safe(form_section.find_element(By.XPATH, ".//p1[text()='Landline No :']/following-sibling::p"))
        promoter_details["PAN Card"] = get_text_safe(form_section.find_element(By.XPATH, ".//p1[text()='PAN Card No :']/following-sibling::p"))
        promoter_details["Company Registration No"] = get_text_safe(form_section.find_element(By.XPATH, ".//p1[text()='Company Registration No :']/following-sibling::p"))
    except Exception as e:
        print(f"Error scraping promoter details for {link}: {e}")

    # Scrape Director Details
    directors = []
    try:
        director_section = driver.find_element(By.ID, "director_det_body")
        director_entries = director_section.find_elements(By.CLASS_NAME, "form_sec")
        for entry in director_entries:
            try:
                director = {
                    "Name": get_text_safe(entry.find_element(By.XPATH, ".//p1[text()='Director / Partner Name :']/following-sibling::p")),
                    "Email": get_text_safe(entry.find_element(By.XPATH, ".//p1[text()='Email ID :']/following-sibling::p"))
                }
                directors.append(director)
            except Exception as e:
                print(f"Error scraping a director entry for {link}: {e}")
    except Exception as e:
        print(f"Error scraping director details for {link}: {e}")

    promoter_details["Directors"] = directors
    results.append(promoter_details)

    # Print the scraped details for the current link
    print("Scraped Details:")
    print(promoter_details)

# Save results to CSV
output_file = "scraped_promoters.csv"
try:
    with open(output_file, "w", newline="", encoding="utf-8") as file:
        fieldnames = ["Type", "Firm Name", "Email", "Mobile 1", "Mobile 2", "Landline", "PAN Card", "Company Registration No", "Directors"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            # Flatten the Directors list for CSV writing
            result["Directors"] = ", ".join([f"{director['Name']} ({director['Email']})" for director in result["Directors"]])
            writer.writerow(result)
    print(f"Scraping completed. Results saved to {output_file}")
except Exception as e:
    print(f"Error saving results to CSV: {e}")

# Close WebDriver
driver.quit()