import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up WebDriver options
chrome_options = Options()
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--ignore-ssl-errors")
driver = webdriver.Chrome(options=chrome_options)

try:
    # Open the URL
    url = "https://www.gujrera.gujarat.gov.in"  # Replace with the actual URL
    driver.get(url)

    # 1. Wait for and click the first link
    first_link = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(
            (By.XPATH, "//div[@id='DataFromJson']//a[@class='figur underlineData' and contains(text(), '14,676')]")
        )
    )
    driver.execute_script("arguments[0].click();", first_link)
    print("Clicked on the first link (14,676).")

    # 2. Wait for and click the second link
    second_link = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(
            (By.XPATH, "//td//a[contains(@href, 'javascript:void(0);')]/strong[text()='4,580']")
        )
    )
    driver.execute_script("arguments[0].click();", second_link)
    print("Clicked on the second link (14,675).")

    # 3. Wait for the table to load and for rows with actual data
    WebDriverWait(driver, 40).until(
        lambda d: len(d.find_elements(By.XPATH, "//tbody/tr[td[1][not(contains(text(), 'Loading'))]]")) > 0
    )
    print("Table loaded with actual data.")

    # 4. Locate the table body
    table_body = driver.find_element(By.TAG_NAME, "tbody")
    rows = table_body.find_elements(By.TAG_NAME, "tr")

    print(f"Found {len(rows)} rows in the table.")

    # 5. Scrape data from all rows in the table
    data = []
    for row in rows:
        # Extract all cells in the row
        cells = row.find_elements(By.TAG_NAME, "td")

        # Ensure there are enough cells (skip incomplete rows)
        if len(cells) >= 11:
            row_data = {
                "Sr No": cells[0].text.strip(),
                "Project Name": cells[1].text.strip(),
                "Promoter Name": cells[2].text.strip(),
                "Address": cells[3].text.strip(),
                "Project Type": cells[4].text.strip(),
                "Email": cells[5].text.strip(),
                "Phone": cells[6].text.strip(),
                "Approval ID": cells[7].text.strip(),
                "City": cells[8].text.strip(),
                "Start Date": cells[9].text.strip(),
                "End Date": cells[10].text.strip(),
                "Remarks": cells[11].text.strip() if len(cells) > 11 else "NA",
            }
            data.append(row_data)

    if not data:
        print("No data scraped. Verify the structure of the table or check if it's dynamically loaded.")

    # Save the scraped data to a CSV file
    with open("scraped_data.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "Sr No",
                "Project Name",
                "Promoter Name",
                "Address",
                "Project Type",
                "Email",
                "Phone",
                "Approval ID",
                "City",
                "Start Date",
                "End Date",
                "Remarks",
            ],
        )
        writer.writeheader()
        writer.writerows(data)

    print("Data successfully scraped and saved to 'scraped_data.csv'.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()
