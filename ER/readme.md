<h1>Maharera Scraper</h1>

  <h2>Project Overview</h2>
    <p>This project is a web scraper designed specifically for automating the collection of Maharera (Maharashtra Real Estate Regulatory Authority) applications in Maharashtra, India. Initially developed using the BeautifulSoup module, it was later enhanced with Selenium to handle dynamic content effectively. The scraper targets approximately 46,700 applications, extracting crucial details about promoters for comprehensive analysis.</p>

  <h2>Features</h2>
    <ul>
        <li><strong>Web Scraping with Selenium:</strong> Utilizes Selenium for navigating and scraping dynamic web pages, essential for handling the complex Maharera application site.</li>
        <li><strong>Data Extraction:</strong> Extracts detailed promoter information including names, contact details, and project affiliations from Maharera applications.</li>
        <li><strong>Data Storage:</strong> Saves the collected data into a CSV file format, ensuring accessibility and ease of further analysis.</li>
    </ul>

  <h2>Requirements</h2>
    <ul>
        <li>Python 3.x</li>
        <li>Selenium</li>
        <li>Pandas</li>
        <li>ChromeDriver</li>
    </ul>

  <h2>Implementation</h2>
    <p>The scraper employs Selenium's capabilities to navigate through the Maharera website, extract relevant hrefs, and subsequently gather promoter details. It utilizes Pandas for structured data handling and ChromeDriver to interface with the Chrome browser for automation tasks.</p>

   <h2>Usage</h2>
    <ol>
        <li><strong>Setup:</strong> Ensure Python 3.x is installed along with required dependencies.</li>
        <li><strong>Execution:</strong> Run the scraper script to initiate the data collection process.</li>
        <li><strong>Output:</strong> Data is saved in a CSV file, facilitating seamless integration with analytical tools or further processing.</li>
    </ol>
