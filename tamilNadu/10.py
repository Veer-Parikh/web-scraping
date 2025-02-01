import csv
import requests
from bs4 import BeautifulSoup

def scrape_data(url):
    try:
        response = requests.get(url, verify=False, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        
        def safe_find_text(text):
            element = soup.find(text=text)
            if element:
                return element.find_next("p").text.strip() if element.find_next("p") else "N/A"
            return "N/A"
        
        data = {
            "URL": url,
            "Project Developed By": safe_find_text("Project Developed by :"),
            "Type of Promoter": safe_find_text("Type of Promoter :"),
            "Firm Name": safe_find_text("Firm Name :"),
            "Email ID": safe_find_text("Email ID :"),
            "Mobile No 1": safe_find_text("Mobile No. 1 :"),
            "PAN Card No": safe_find_text("PAN Card No :"),
            "Company Registration No": safe_find_text("Company Registration No :"),
        }

        # Extract the directors' details
        directors_section = soup.find("div", id="director_det_body")
        directors_data = []

        if directors_section:
            director_entries = directors_section.find_all("div", class_="form_sec")
            for entry in director_entries:
                director_name = entry.find(text="Director / Partner Name :")
                email = entry.find(text="Email ID :")
                mobile_1 = entry.find(text="Mobile No. 1 :")
                mobile_2 = entry.find(text="Mobile No. 2 :")
                address = entry.find(text="Address :")
                photo_tag = entry.find("a", class_="fa-file-text-o")

                directors_data.append({
                    "Name": director_name.find_next("p").text.strip() if director_name else "N/A",
                    "Email": email.find_next("p").text.strip() if email else "N/A",
                    "Mobile No. 1": mobile_1.find_next("p").text.strip() if mobile_1 else "N/A",
                    "Mobile No. 2": mobile_2.find_next("p").text.strip() if mobile_2 else "N/A",
                    "Address": address.find_next("p").text.strip() if address else "N/A",
                    "Photo URL": photo_tag["href"] if photo_tag else "N/A",
                })
        
        data["Directors"] = directors_data  # Store the directors' data in the main dictionary

        return data

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

# Input CSV containing the URLs
input_file = "final.csv"
scraped_data = []
promoter_links = []

# Read URLs from the CSV file
with open(input_file, "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader, None)  # Skip header row if exists
    for row in reader:
        if row and len(row) > 0:  # Skip empty rows
            promoter_links.append(row[0])

# Scrape data from each URL
for url in promoter_links:
    print(f"Scraping data from: {url}")
    data = scrape_data(url)
    if data:
        scraped_data.append(data)

# Write scraped data to a new CSV file
output_file = "scraped_data_directors1.csv"
with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
    fieldnames = ["URL", "Project Developed By", "Type of Promoter", "Firm Name", 
                  "Email ID", "Mobile No 1", "PAN Card No", "Company Registration No", "Directors"]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    
    for row in scraped_data:
        row["Directors"] = str(row["Directors"])  # Convert list to string for CSV storage
        writer.writerow(row)

print(f"Scraping complete. Data saved to '{output_file}'.")
