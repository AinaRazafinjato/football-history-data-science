from scrapers import WebScraper, scrape_league, scrape_all_leagues
import argparse
import sys
from loguru import logger

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Scrape football data from fbref.com")
    parser.add_argument("--league", "-l", help="League key to scrape (e.g. premier_league)")
    parser.add_argument("--url", "-u", help="Custom URL to scrape")
    parser.add_argument("--all", "-a", action="store_true", help="Scrape all leagues")
    parser.add_argument("--historical", action="store_true", help="Scrape historical data")
    parser.add_argument("--no-save", action="store_true", help="Don't save to CSV files")
    parser.add_argument("--config", "-c", default="config_url.yaml", help="Path to config file")
    return parser.parse_args()

def main():
    """Main function to run the scraper from command line."""
    args = parse_args()
    
    try:
        save = not args.no_save
        
        if args.all:
            logger.info("Scraping all leagues")
            results = scrape_all_leagues(save=save, config_path=args.config)
            logger.success(f"Successfully scraped {len(results)} leagues")
            # You can add more code to work with results here if needed
        
        elif args.historical:
            logger.info("Scraping historical data")
            scraper = WebScraper(config_path=args.config)
            results = scraper.scrape_historical_data()
            logger.success(f"Successfully scraped {len(results)} historical seasons")
            # You can add more code to work with results here if needed
            
        elif args.url:
            logger.info(f"Scraping custom URL: {args.url}")
            # Use the result instead of just calling the function
            data = scrape_league(url=args.url, save=save, config_path=args.config)
            logger.success(f"Successfully scraped data from custom URL: {data.shape[0]} rows")
            
        elif args.league:
            logger.info(f"Scraping league: {args.league}")
            # Use the result instead of just calling the function
            data = scrape_league(league_key=args.league, save=save, config_path=args.config)
            logger.success(f"Successfully scraped {args.league} data: {data.shape[0]} rows")
            
        else:
            # Default behavior - use default league from config
            scraper = WebScraper(config_path=args.config)
            # Use the result instead of just calling the function
            data = scraper.parse_data()
            
            if save:
                scraper.save_to_csv()
                
            logger.success(f"Successfully scraped default league data: {data.shape[0]} rows")
            
        return 0
        
    except Exception as e:
        logger.error(f"Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())