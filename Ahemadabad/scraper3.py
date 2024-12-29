from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

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
            (By.XPATH, "//td//a[contains(@href, 'javascript:void(0);')]/strong[text()='14,675']")
        )
    )
    driver.execute_script("arguments[0].click();", second_link)
    print("Clicked on the second link (14,675).")

    # Optional: Add delay to observe the result
    time.sleep(1000)

except Exception as e:
    print(f"Error: {e}")
    driver.save_screenshot("error_debug.png")
finally:
    driver.quit()
