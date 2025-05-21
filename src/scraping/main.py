from .config import URL
from src.scraping.scrapers import WebScraper
    
# Create a scraper instance with a FBref URL
scraper = WebScraper(URL)

# Parse the data
df = scraper.parse_data()

# Save data to CSV
scraper.save_to_csv()