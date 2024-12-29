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
current_page = 1
start_scraping_page = 1000  # Start scraping from this page
total_pages = 1468  # Total pages to scrape

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
            (By.XPATH, "//td//a[contains(@href, 'javascript:void(0);')]/strong[text()='14,675']")
        )
    )
    driver.execute_script("arguments[0].click();", second_link)
    print("Clicked on the second link (14,675).")

    # Prepare CSV file for writing
    with open("scraped_data2.csv", mode="w", newline="", encoding="utf-8") as file:
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

        # Traverse to the start_scraping_page (1000th page)
        while current_page < start_scraping_page:
            print(f"Navigating to page {current_page + 1}...")
            try:
                next_page_button = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, f"//ul[@class='ngx-pagination']//a[span[text()='{current_page + 1}']]")
                    )
                )
                driver.execute_script("arguments[0].click();", next_page_button)

                # Wait for the page to load and confirm the navigation
                WebDriverWait(driver, 10).until(
                    lambda d: d.find_element(By.XPATH, f"//ul[@class='ngx-pagination']//li[@class='current' and span[text()='{current_page + 1}']]")
                )
                current_page += 1
            except Exception as e:
                print(f"Error navigating to page {current_page + 1}: {e}")
                break

        print(f"Reached page {start_scraping_page}. Starting scraping...")

        # Start scraping from the 1000th page
        while current_page <= total_pages:
            print(f"Scraping data from page {current_page}...")

            # Wait for the table rows to load
            WebDriverWait(driver, 40).until(
                lambda d: len(d.find_elements(By.XPATH, "//tbody/tr[td[1][not(contains(text(), 'Loading'))]]")) > 0
            )

            # Locate the table body and scrape rows
            table_body = driver.find_element(By.TAG_NAME, "tbody")
            rows = table_body.find_elements(By.TAG_NAME, "tr")

            print(f"Found {len(rows)} rows in the table on page {current_page}.")

            # Scrape data from all rows in the table
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

            # Write data to CSV
            writer.writerows(data)

            # Calculate the next page number with formatting
            if current_page >= 1000:
                next_page_label = f"1,{current_page - 999}"
            else:
                next_page_label = str(current_page + 1)

            current_page += 1
            if current_page > total_pages:
                print("All pages scraped successfully.")
                break

            # Try to click on the next page number
            try:
                next_page_button = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, f"//ul[@class='ngx-pagination']//a[span[text()='{next_page_label}']]")
                    )
                )
                driver.execute_script("arguments[0].click();", next_page_button)

                # Wait for the page to load and confirm navigation
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, f"//ul[@class='ngx-pagination']//li[@class='current' and span[text()='{next_page_label}']]")
                    )
                )
                print(f"Navigated to page {current_page}.")
            except Exception as e:
                print(f"Error navigating to page {current_page}: {e}")

    print("All pages scraped successfully.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()
