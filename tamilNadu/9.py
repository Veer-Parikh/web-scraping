import csv
import requests
from bs4 import BeautifulSoup

# Function to scrape data from a given URL
def scrape_data(url):
    try:
        # Fetch the page content (disable SSL verification)
        response = requests.get(url, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Helper function to safely extract text
        def safe_find_text(text):
            element = soup.find(text=text)
            if element:
                return element.find_next("p").text.strip() if element.find_next("p") else "N/A"
            return "N/A"
        
        # Extract the required data using the safe_find_text function
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
        return data
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

input_file = "final.csv"
scraped_data = []
promoter_links = []
with open(input_file, "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader, None)  # Skip header row if exists
    for row in reader:
        if row and len(row) > 0:  # Skip empty rows
            promoter_links.append(row[0])

# Scraping data from each URL
for url in promoter_links:
    print(f"Scraping data from: {url}")
    data = scrape_data(url)
    if data:
        scraped_data.append(data)

# Writing scraped data to a new CSV file
with open('scraped_data1.csv', mode='w', newline='', encoding='utf-8') as outfile:
    fieldnames = ["URL", "Project Developed By", "Type of Promoter", "Firm Name", 
                  "Email ID", "Mobile No 1", "PAN Card No", "Company Registration No"]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in scraped_data:
        writer.writerow(row)

print("Scraping complete. Data saved to 'scraped_data.csv'.")
