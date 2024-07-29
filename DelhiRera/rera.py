from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

driver = webdriver.Chrome()

# Open the URL
url = 'https://www.rera.delhi.gov.in/registered_promoters_list?combine_1=&items_per_page=All'
driver.get(url)

# Allow the page to load completely
driver.implicitly_wait(10)

data = []

try:
    # Find the main container
    #main_container = driver.find_element(By.CLASS_NAME, 'view.view-clone-of-promoters-list.view-id-clone_of_promoters_list.view-display-id-page_11.view-dom-id-8851a13b5c41e7a9b71cffa45ac55f30')
    
    # Find the content area
    content_area = driver.find_element(By.CLASS_NAME, 'view-content')
    
    # Find all odd and even elements
    rows = content_area.find_elements(By.CLASS_NAME, 'odd') + content_area.find_elements(By.CLASS_NAME, 'even')
    
    # Loop through each row and extract data
    for row in rows:
        try:
            promoter_info = row.find_element(By.CLASS_NAME, 'views-field-php-1')
            text = promoter_info.get_attribute('innerText').strip()
            
            name = text.split('Name : ')[1].split('Address : ')[0].strip()
            address = text.split('Address : ')[1].split('Email : ')[0].strip()
            email = text.split('Email : ')[1].split('Phone Number : ')[0].strip()
            phone = text.split('Phone Number : ')[1].split('View Photos')[0].strip()
            
            data.append({
                'Name': name,
                'Address': address,
                'Email': email,
                'Phone Number': phone
            })
        except Exception as e:
            print(f"Error extracting data for a row: {e}")
    
    # Create a DataFrame and save to CSV
    df = pd.DataFrame(data)
    df.to_csv('rera_data.csv', index=False)
    print('Data saved to rera_data.csv')

except Exception as e:
    print(f"Error: {e}")

# Close the driver
driver.quit()
