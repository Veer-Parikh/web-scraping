import csv
import requests
from bs4 import BeautifulSoup

# Function to scrape data from a given URL
def scrape_data(url):
    try:
        # Fetch the page content (disable SSL verification)
        response = requests.get(url, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extract the required data
        data = {
            # "URL": url,
            "Project Developed By": soup.find(text="Project Developed by :").find_next("p").text.strip(),
            "Type of Promoter": soup.find(text="Type of Promoter :").find_next("p").text.strip(),
            "Firm Name": soup.find(text="Firm Name :").find_next("p").text.strip(),
            "Email ID": soup.find(text="Email ID :").find_next("p").text.strip(),
            "Mobile No 1": soup.find(text="Mobile No. 1 :").find_next("p").text.strip(),
            "PAN Card No": soup.find(text="PAN Card No :").find_next("p").text.strip(),
            "Company Registration No": soup.find(text="Company Registration No :").find_next("p").text.strip(),
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
with open('scraped_data.csv', mode='w', newline='', encoding='utf-8') as outfile:
    fieldnames = ["Project Developed By", "Type of Promoter", "Firm Name", 
                  "Email ID", "Mobile No 1", "PAN Card No", "Company Registration No"]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in scraped_data:
        writer.writerow(row)

print("Scraping complete. Data saved to 'scraped_data.csv'.")
