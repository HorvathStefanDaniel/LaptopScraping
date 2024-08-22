import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

# Define headers to mimic a browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
}

# URL of the page to scrape (Newegg laptop search with some filters applied)
base_url = "https://www.newegg.com/p/pl?d=laptop&LeftPriceRange=300+1000&PageSize=96&page={page}"

# Function to scrape laptop data
def scrape_laptops(url, page_number):
    laptops = []
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the relevant section in the HTML
        laptop_items = soup.find_all('div', class_='item-cell')
        
        print(f"Found {len(laptop_items)} laptops on page {page_number}.")

        for item in laptop_items:
            name = item.find('a', class_='item-title')
            if not name:
                continue
            name = name.text.strip()
            
            # Attempt to find release date or set to unknown
            release_date_elem = item.find('li', string='Release Date')
            release_date = release_date_elem.find_next_sibling('li').text.strip() if release_date_elem else "Unknown"
            
            features = item.find('ul', class_='item-features')
            
            if 'fingerprint' in name.lower():
                has_fingerprint = True
            else: 
                if features:
                    features = features.text.strip()
                    has_fingerprint = 'fingerprint' in features.lower()
                else:
                    has_fingerprint = False
            
            laptops.append({
                'Name': name,
                'Release Date': release_date,
                'Fingerprint Scanner': has_fingerprint,
                'Page': page_number  # Add the page number here
            })
        
        # Random sleep to mimic human behavior
        time.sleep(random.uniform(1, 3))
    
    except requests.RequestException as e:
        print(f"An error occurred with the request for {url}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while parsing {url}: {e}")
    
    return laptops

# Number of pages to scrape
max_pages = 20  # Adjust this value based on how many pages you want to scrape

# Run the scraper
all_laptops = []
for page in range(1, max_pages + 1):
    url = base_url.format(page=page)
    all_laptops.extend(scrape_laptops(url, page))

# Convert to DataFrame
df = pd.DataFrame(all_laptops)

# Output the results
print(df)

# Save to CSV
df.to_csv('laptop_data_newegg.csv', index=False, header=True)
