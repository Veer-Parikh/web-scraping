import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    # Send an HTTP GET request to the website
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Get the entire HTML content
        html_content = soup.prettify()
        
        # Save the HTML content to a file
        with open('scraped_page.html', 'w', encoding='utf-8') as file:
            file.write(html_content)
        
        print(f"HTML content has been saved to 'scraped_page.html'")
    else:
        print(f"Failed to retrieve the website. Status code: {response.status_code}")

# Example usage
url = 'https://rera.karnataka.gov.in/projectViewDetails'
scrape_website(url)
