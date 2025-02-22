import logging
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# List of areas (stations) in Mumbai
mumbai_landmarks = {
    "Churchgate": [
        "Gateway of India", "Nariman Point", "Marine Drive",
        "Veer Nariman Road", "Fort Area", "CR2 Mall",
        "Express Towers", "Maker Chambers", "Mantralaya"
    ],
    "Marine Lines": [
        "Marine Drive", "Taraporewala Aquarium", "Wankhede Stadium",
        "Maharshi Karve Road", "Princess Street", "Metro INOX Cinema"
    ],
    "Charni Road": [
        "Girgaon Chowpatty", "Babulnath Temple", "Opera House",
        "Jagannath Shankar Sheth Road", "Hughes Road", "SoBo Central Mall"
    ],
    "Grant Road": [
        "Lamington Road", "Nana Chowk", "Falkland Road",
        "Heera Panna Market", "Novelty Cinema"
    ],
    "Mumbai Central": [
        "Nair Hospital", "Maratha Mandir Theatre", "Agripada",
        "Bellasis Road", "Tulsiwadi", "Mumbai Central Bus Depot"
    ],
    "Mahalaxmi": [
        "Mahalaxmi Temple", "Racecourse", "Haji Ali Dargah",
        "Dr. E. Moses Road", "Jacob Circle", "High Street Phoenix Mall"
    ],
    "Lower Parel": [
        "Kamala Mills", "Todi Mills", "Senapati Bapat Marg",
        "Palladium Mall", "Indiabulls Finance Center", "One Indiabulls"
    ],
    "Prabhadevi": [
        "Siddhivinayak Temple", "Dadar Beach", "Century Bazaar",
        "Veer Savarkar Road", "Gokhale Road"
    ],
    "Dadar": [
        "Shivaji Park", "Plaza Cinema", "Portuguese Church",
        "Senapati Bapat Marg", "Dadar TT Circle", "Kabutar Khana"
    ],
    "Matunga": [
        "Five Gardens", "King’s Circle", "Shanmukhananda Hall",
        "Ambedkar Road", "Matunga Market"
    ],
    "Sion": [
        "Sion Fort", "Sion Hospital", "Gurukripa Restaurant",
        "Sion Circle", "Everard Nagar"
    ],
    "Kurla": [
        "Phoenix Market City", "BKC Connector", "Kalina",
        "LBS Road", "Nehru Nagar", "Kurla Kamani"
    ],
    "Vidya Vihar": [
        "Somaiya College", "Vidyavihar East", "Rajawadi Hospital"
    ],
    "Ghatkopar": [
        "R City Mall", "Ghatkopar Depot", "Pant Nagar",
        "90 Feet Road", "Rajawadi", "Garodia Nagar"
    ],
    "Vikhroli": [
        "Godrej Colony", "Tagore Nagar", "LBS Marg",
        "Hiranandani Link Road", "Vikhroli Parksite"
    ],
    "Kanjurmarg": [
        "Hiranandani Powai", "Eastern Express Highway",
        "LBS Marg", "Kanjurmarg East"
    ],
    "Bhandup": [
        "Dreams Mall", "Tata Colony", "LBS Road",
        "Bhandup Station Road", "Nahur Village"
    ],
    "Nahur": [
        "Mulund Colony", "Sarvodaya Nagar", "Nahur East"
    ],
    "Mulund": [
        "R Mall", "Nirmal Lifestyle", "LBS Marg",
        "Mulund Check Naka", "Mulund Goregaon Link Road"
    ],
    "Thane": [
        "Viviana Mall", "Korum Mall", "Upvan Lake",
        "Eastern Express Highway", "Majiwada", "Kopri"
    ],
    "Kalwa": [
        "Kharegaon", "Parsik Nagar", "Kalwa Bridge"
    ],
    "Mumbra": [
        "Mumbra Devi Temple", "Kausa", "Shilphata Road"
    ],
    "Diva": [
        "Diva Gaon", "Mothagaon", "Sonar Pada"
    ],
    "Kopar": [
        "Dombivli MIDC", "Manpada Road"
    ],
    "Dombivli": [
        "Tilak Nagar", "Dombivli Gymkhana", "Ganpati Mandir",
        "Phadke Road", "Dombivli East-West Bridge"
    ],
    "Thakurli": [
        "Shivaji Udyan", "Dattanagar"
    ],
    "Kalyan": [
        "Sarvoday Mall", "Metro Junction Mall", "Gandhari Bridge",
        "Shivaji Chowk", "Khadegolwadi"
    ],
    "Shahad": [
        "Ulhas River", "Birla Mandir", "Shahad Railway Colony"
    ],
    "Ambivli": [
        "Titwala Road", "Ambivli MIDC"
    ],
    "Titwala": [
        "Titwala Ganpati Temple", "Kalu River"
    ],
    "Khadavli": [
        "Godrej Hill", "Khadavli River"
    ],
    "Vasind": [
        "Tansa River", "Vasind MIDC"
    ],
    "Asangaon": [
        "Manas Mandir", "Shahapur"
    ],
    "Atgaon": [
        "Atgaon Industrial Area"
    ],
    "Bhivpuri Road": [
        "Bhivpuri Waterfall", "Karjat Road"
    ],
    "Karjat": [
        "ND Studios", "Bhivpuri Dam", "Matheran Toy Train Station"
    ],
    "Palasdari": [
        "Palasdari Dam"
    ],
    "Kelavali": [
        "Kelavali Village"
    ],
    "Dolavali": [
        "Dolavali MIDC"
    ],
    "Lowjee": [
        "Lowjee Hill"
    ],
    "Khopoli": [
        "Imagica Theme Park", "Khopoli Waterfalls"
    ],
    "Sandhurst Road": [
        "Dongri", "Pydhonie", "Bhendi Bazaar"
    ],
    "Masjid": [
        "Crawford Market", "Mangaldas Market"
    ],
    "CST": [
        "Chhatrapati Shivaji Terminus", "Flora Fountain"
    ],
    "Wadala Road": [
        "IMAX Dome", "BPT Colony"
    ],
    "GTB Nagar": [
        "GTB Hospital", "Dadar TT"
    ],
    "Chunabhatti": [
        "EEH Flyover", "Koliwada"
    ],
    "Tilaknagar": [
        "Tilaknagar Police Station"
    ],
    "Chembur": [
        "Diamond Garden", "Chembur Gymkhana"
    ],
    "Govandi": [
        "Deonar Dumping Ground"
    ],
    "Mankhurd": [
        "Mankhurd Shivaji Nagar"
    ],
    "Vashi": [
        "Inorbit Mall", "Palm Beach Road"
    ],
    "Sanpada": [
        "Millennium Business Park"
    ],
    "Juinagar": [
        "D Y Patil Stadium"
    ],
    "Nerul": [
        "Seawoods Grand Central"
    ],
    "Seawoods-Darave": [
        "Navi Mumbai Golf Course"
    ],
    "Belapur": [
        "CBD Belapur"
    ],
    "Kharghar": [
        "Kharghar Hills", "Central Park"
    ],
    "Mansarovar": [
        "Mansarovar Railway Station"
    ],
    "Khandeshwar": [
        "Khandeshwar Lake"
    ],
    "Panvel": [
        "Orion Mall", "Panvel Fort"
    ],
    "Bandra-Kurla Complex (BKC)": {
        "Landmarks": ["Jio World Centre", "MMRDA Grounds", "U.S. Consulate", "Asian Heart Institute"],
        "Roads": ["BKC Connector", "Santacruz-Chembur Link Road (SCLR)"],
        "Business Centers": ["One BKC", "The Capital", "Naman Chambers", "Platina", "G Block Business Hub"]
    },
    "Elphinstone Road (Prabhadevi)": {
        "Landmarks": ["Indiabulls Finance Centre", "Peninsula Corporate Park"],
        "Roads": ["Senapati Bapat Marg", "Tulsi Pipe Road"],
        "Business Centers": ["Lodha Supremus", "One Indiabulls Centre"]
    },
    "Mahim": {
        "Landmarks": ["Mahim Causeway", "St. Michael’s Church", "Shivaji Park Extension"],
        "Roads": ["L.J. Road", "Cadell Road"]
    },
    "Bandra": {
        "Landmarks": ["Bandra-Worli Sea Link", "Mount Mary Church", "Bandra Fort"],
        "Roads": ["Linking Road", "Hill Road", "Carter Road", "Bandra-Kurla Complex Road"]
    },
    "Khar Road": {
        "Landmarks": ["Khar Gymkhana", "Pali Hill"],
        "Roads": ["S.V. Road", "14th Road"]
    },
    "Santacruz": {
        "Landmarks": ["Grand Hyatt", "Santacruz Airport Terminal"],
        "Roads": ["Western Express Highway", "Milan Subway"]
    },
    "Vile Parle": {
        "Landmarks": ["NMIMS University", "Cooper Hospital", "Juhu Beach"],
        "Roads": ["S.V. Road", "Juhu Tara Road"]
    },
    "Jogeshwari": {
        "Landmarks": ["Jogeshwari Caves", "Western Express Highway Flyover"]
    },
    "Goregaon": {
        "Landmarks": ["Oberoi Mall", "Film City"],
        "Roads": ["Aarey Road"]
    },
    "Malad": {
        "Landmarks": ["Inorbit Mall", "Infinity Mall"],
        "Business Centers": ["Mindspace Malad"]
    },
    "Kandivali": {
        "Landmarks": ["Growels 101 Mall", "Lokhandwala Township"],
        "Roads": ["Mahavir Nagar"]
    },
    "Borivali": {
        "Landmarks": ["Sanjay Gandhi National Park"],
        "Roads": ["IC Colony", "Shimpoli", "Chandavarkar Road"]
    },
    "Dahisar": {
        "Landmarks": ["Dahisar Check Naka"],
        "Roads": ["Anand Nagar", "S V Road"]
    },
    "Mira Road": {
        "Landmarks": ["Shanti Nagar", "GCC Club", "Beverly Park"]
    },
    "Bhayandar": {
        "Landmarks": ["Maxus Mall", "Jesal Park"],
        "Roads": ["Golden Nest"]
    },
    "Naigaon": {
        "Landmarks": ["Juchandra Road"]
    },
    "Vasai Road": {
        "Landmarks": ["Bassein Fort", "Vasai Industrial Area"],
        "Roads": ["Stella Maris Hospital"]
    }
}



# Start WebDriver
logging.info("Starting the WebDriver...")
driver = webdriver.Chrome()

def scroll_down(scrollable_element, pause_time=3, max_scrolls=30):
    scrolls = 0
    logging.info("Scrolling through search results...")
    while scrolls < max_scrolls:
        try:
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_element)
            time.sleep(pause_time)
            scrolls += 1
        except Exception as e:
            logging.error("Scrolling error: %s", e)
            break

# Initialize results storage
all_href_links = []

# Iterate over each area in Mumbai
for area in mumbai_landmarks:
    logging.info(f"Searching for real estate agents in {area}...")
    search_url = f"https://www.google.com/maps/search/real+estate+agents+in+{area}+Mumbai/"
    driver.get(search_url)
    time.sleep(10)

    # Locate the scrollable div
    try:
        scrollable_div = driver.find_element(By.XPATH, "//div[contains(@aria-label, 'Results for')]")
        logging.info("Scrollable div located.")
        scroll_down(scrollable_div)
    except Exception as e:
        logging.error("Failed to locate the scrollable div: %s", e)
        continue

    # Extracting Href Links
    business_elements = driver.find_elements(By.CLASS_NAME, "Nv2PK")
    logging.info(f"Found {len(business_elements)} business listings in {area}.")
    
    for element in business_elements:
        try:
            link_element = element.find_element(By.TAG_NAME, "a")
            href = link_element.get_attribute("href")
            if href:
                all_href_links.append({"Area": area, "URL": href})
                logging.info(f"Extracted: {href}")
        except Exception as e:
            logging.error(f"Error extracting href: {e}")
            continue

# Save to CSV
df = pd.DataFrame(all_href_links)
df.to_csv("real_estate_links_mumbai.csv", index=False)
logging.info("Data saved to 'real_estate_links_mumbai.csv'.")

# Close the browser
driver.quit()


# andhra pradesh, gujarat (remaining cities only), himachal pradesh, karnataka, kerala, MP (remaining cities only), punjab, rajasthan (remaining cities only), telangana, west bengal