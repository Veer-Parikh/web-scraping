from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Initialize WebDriver
driver = webdriver.Chrome()

# Navigate to the website
url = "https://www.up-rera.in/promoters"
driver.get(url)

# Function to scrape data from the current page
def scrape_current_page():
    table = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_grdagents")
    rows = table.find_elements(By.TAG_NAME, "tr")[1:]  # Skip the header row
    page_data = []

    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        if cells:
            data = {
                "SNo": cells[0].text,
                "Reg.Number": cells[1].text,
                "Name": cells[2].text,
                "Address": cells[3].text,
                "Mobile": cells[4].text.split('\n')[0],
                "Email": cells[4].text.split('\n')[1] if '\n' in cells[4].text else '',
                "Website": cells[4].find_element(By.TAG_NAME, "a").get_attribute("href") if cells[4].find_elements(By.TAG_NAME, "a") else '',
                "Type": cells[5].text
            }
            page_data.append(data)
    return page_data

# Scrape all pages (1 to 39)
all_data = []

for page in range(1, 40):  # Page 1 to 39
    print(f"Scraping page {page}...")
    # Scrape data from the current page
    all_data.extend(scrape_current_page())

    # Go to the next page if not the last page
    if page < 39:
        script = f"__doPostBack('ctl00$ContentPlaceHolder1$grdagents','Page${page + 1}')"
        driver.execute_script(script)
        time.sleep(3)  # Wait for the page to load

# Convert the data into a pandas DataFrame
df = pd.DataFrame(all_data)

# Save the data to a CSV file
df.to_csv("up_rera_promoters.csv", index=False)

print("Data has been saved to up_rera_promoters.csv")

# Close the browser
driver.quit()
