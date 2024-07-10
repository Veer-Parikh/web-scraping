Maharera Scraper
This project is a web scraper designed to automate the collection of Maharera applications present in Maharashtra. Initially developed using the BeautifulSoup module, it was later enhanced with Selenium to accommodate the need for automation and dynamic content handling. The scraper collects hrefs from approximately 46,700 applications, checks for the presence of promoters, and extracts all necessary details of the promoters. The final output is stored in a CSV file for further analysis and use.

Features
Web Scraping with Selenium: Utilizes Selenium for dynamic web content handling and automation.
Data Extraction: Extracts detailed promoter information from Maharera applications.
Data Storage: Stores the collected data in a CSV file for easy access and analysis.
Requirements
Python 3.x
Selenium
Pandas
ChromeDriver