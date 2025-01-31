import csv
import requests
import pandas as pd
from bs4 import BeautifulSoup
import requests
import certifi



input_file = "final.csv"
scraped_data = []
promoter_links = []
with open(input_file, "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader, None)  # Skip header row if exists
    for row in reader:
        if row and len(row) > 0:  # Skip empty rows
            promoter_links.append(row[0])  # First column (Promoter Details)

# Print extracted links for debugging
# print("Extracted Promoter Links:", promoter_links)

for url in promoter_links:
    try:
        response = requests.get(url, verify=certifi.where())

        print(f"Scraping: {url}")
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract relevant details using text matching and class names
        data = {
            "URL": url,
            "Project Developed By": soup.find(text="Project Developed by :").find_next("p").text.strip(),
            "Type of Promoter": soup.find(text="Type of Promoter :").find_next("p").text.strip(),
            "Firm Name": soup.find(text="Firm Name :").find_next("p").text.strip(),
            "Email ID": soup.find(text="Email ID :").find_next("p").text.strip(),
            "Mobile No 1": soup.find(text="Mobile No. 1 :").find_next("p").text.strip(),
            "PAN Card No": soup.find(text="PAN Card No :").find_next("p").text.strip(),
            "Company Registration No": soup.find(text="Company Registration No :").find_next("p").text.strip(),
        }

        # Extract Address
        address_section = soup.find(text="Address :").find_next("p").text.strip()
        data["Address"] = " ".join(address_section.split())

        # Extract links
        links = soup.find_all("a", href=True)
        data["PAN Card File"] = links[-2]["href"] if len(links) > 1 else "N/A"
        data["Registration Certificate"] = links[-1]["href"] if len(links) > 1 else "N/A"

        scraped_data.append(data)

    except Exception as e:
        print(f"Failed to scrape {url}: {e}")

# Save data to CSV
output_csv = "scraped_data.csv"
pd.DataFrame(scraped_data).to_csv(output_csv, index=False)
print(f"Scraping complete! Data saved to {output_csv}")