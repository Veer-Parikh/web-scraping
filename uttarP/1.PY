from selenium import webdriver
from selenium.webdriver.common.by import By

# Initialize the WebDriver (use the path to your WebDriver)
driver = webdriver.Chrome()

# Navigate to the website
url = "https://www.up-rera.in/promoters"
driver.get(url)

# Find the table by ID
table = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_grdagents")

# Extract all rows except the header
rows = table.find_elements(By.TAG_NAME, "tr")[1:]  # Skip the header row

# Data storage
scraped_data = []

# Iterate through rows
for row in rows:
    cells = row.find_elements(By.TAG_NAME, "td")
    if cells:
        data = {
            "SNo": cells[0].text,
            "Reg.Number": cells[1].text,
            "Name": cells[2].text,
            "Address": cells[3].text,
            "Contact Details": {
                "Mobile": cells[4].text.split('\n')[0],
                "Email": cells[4].text.split('\n')[1] if '\n' in cells[4].text else '',
                "Website": cells[4].find_element(By.TAG_NAME, "a").get_attribute("href") if cells[4].find_elements(By.TAG_NAME, "a") else '',
            },
            "Type": cells[5].text
        }
        scraped_data.append(data)

# Print or save the data
for entry in scraped_data:
    print(entry)

# Close the browser
driver.quit()
