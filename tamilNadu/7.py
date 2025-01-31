import requests
from bs4 import BeautifulSoup

# URL to scrape
url = "https://rera.tn.gov.in/public-view1/building/pfirm/5bb5f080-69fa-11ef-9518-dfae184febe2"

# Fetch the page content (disable SSL verification)
response = requests.get(url, verify=False)

# Parse the HTML content
soup = BeautifulSoup(response.text, "html.parser")

# Extract the required data
try:
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

    # Print the extracted data
    print(data)

except AttributeError:
    print("Some elements were not found on the page. Check the HTML structure.")

