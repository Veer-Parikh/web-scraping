from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_data(driver, url):
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

        # Parse and print the table content
        for row in rows:
            columns = row.find_elements(By.XPATH, ".//td")
            if columns:
                email = columns[0].text
                name = columns[1].text
                address = columns[2].text
                contact = columns[3].text
                print(f"Email: {email}, Name: {name}, Address: {address}, Contact: {contact}")

    except Exception as e:
        print(f"Error scraping {url}: {e}")

# Selenium setup
driver = webdriver.Chrome()  # Adjust if using a different browser
urls = [
    "https://rera.rajasthan.gov.in/Home/ViewProject?id=GMdALZLTwHw=&type=U",
    "https://rera.rajasthan.gov.in/Home/ViewProject?id=4I4DIqGM+S0=&type=U",
    # Add other URLs as needed
]

for i, url in enumerate(urls[:10], start=1):  # Limit to first 10 links
    print(f"Scraping {i}/{len(urls)}: {url}")
    scrape_data(driver, url)

driver.quit()
