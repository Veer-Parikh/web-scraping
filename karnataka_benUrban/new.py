from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
driver = webdriver.Chrome()

# Open the URL
url = 'https://rera.karnataka.gov.in/projectViewDetails'
driver.get(url)
time.sleep(3)
