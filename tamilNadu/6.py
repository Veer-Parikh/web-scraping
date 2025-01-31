import csv
import requests
import pandas as pd
from bs4 import BeautifulSoup
import certifi
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# Function to create a requests session with retries
def create_session():
    session = requests.Session()
    retries = Retry(
        total=5,  # Retry up to 5 times
        backoff_factor=1,  # Wait 1s, 2s, 4s, etc. between retries
        status_forcelist=[500, 502, 503, 504],  # Retry on these HTTP errors
        allowed_methods=["GET"],  # Retry only GET requests
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("https://", adapter)
    return session


# Read promoter links from CSV
input_file = "final.csv"
promoter_links = []
with open(input_file, "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader, None)  # Skip header row if exists
    for row in reader:
        if row and len(row) > 0:  # Skip empty rows
            promoter_links.append(row[0])  # First column (Promoter Details)

# Print extracted links for debugging
# print("Extracted Promoter Links:", promoter_links)

scraped_data = []
session = create_session()

for url in promoter_links:
    try:
        print(f"Scraping: {url}")
        response = session.get(url, verify=False, timeout=10)  # Set a timeout
        response.raise_for_status()  # Raise error for bad responses (4xx, 5xx)

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract relevant details using text matching and class names
        data = {
            "URL": url,
            "Project Developed By": soup.find(text="Project Developed by :").find_next("p").text.strip() if soup.find(text="Project Developed by :") else "N/A",
            "Type of Promoter": soup.find(text="Type of Promoter :").find_next("p").text.strip() if soup.find(text="Type of Promoter :") else "N/A",
            "Firm Name": soup.find(text="Firm Name :").find_next("p").text.strip() if soup.find(text="Firm Name :") else "N/A",
            "Email ID": soup.find(text="Email ID :").find_next("p").text.strip() if soup.find(text="Email ID :") else "N/A",
            "Mobile No 1": soup.find(text="Mobile No. 1 :").find_next("p").text.strip() if soup.find(text="Mobile No. 1 :") else "N/A",
            "PAN Card No": soup.find(text="PAN Card No :").find_next("p").text.strip() if soup.find(text="PAN Card No :") else "N/A",
            "Company Registration No": soup.find(text="Company Registration No :").find_next("p").text.strip() if soup.find(text="Company Registration No :") else "N/A",
        }

        # Extract Address
        address_section = soup.find(text="Address :")
        data["Address"] = address_section.find_next("p").text.strip() if address_section else "N/A"

        # Extract links
        links = soup.find_all("a", href=True)
        data["PAN Card File"] = links[-2]["href"] if len(links) > 1 else "N/A"
        data["Registration Certificate"] = links[-1]["href"] if len(links) > 1 else "N/A"

        scraped_data.append(data)

    except requests.exceptions.SSLError as ssl_err:
        print(f"SSL error for {url}. Skipping. Error: {ssl_err}")

    except requests.exceptions.RequestException as req_err:
        print(f"Request failed for {url}. Error: {req_err}")

    except Exception as e:
        print(f"Failed to scrape {url}: {e}")

# Save data to CSV
output_csv = "scraped_data.csv"
pd.DataFrame(scraped_data).to_csv(output_csv, index=False)
print(f"Scraping complete! Data saved to {output_csv}")
