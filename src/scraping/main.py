from scrapers import WebScraper, scrape_league, scrape_all_leagues, load_config
import argparse
import sys
import os
from pathlib import Path
from loguru import logger

def setup_logger(config_path="config_url.yaml", verbose=False):
    """Configure the logger based on config settings."""
    config = load_config(config_path)
    log_config = config.get("logging", {})
    
    # Define logs directory
    log_dir = Path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                              log_config.get("log_dir", "logs")))

    # Create logs directory if it doesn't exist
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Remove default configuration
    logger.remove()
    
    # Get formats
    console_format = log_config.get("console_format", 
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>")
    file_format = log_config.get("file_format", 
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>")
    
    # File logger
    log_file = os.path.join(log_dir, log_config.get("log_file_template", "scraping_{time:YYYY-MM-DD}.log"))
    logger.add(
        log_file,
        rotation=log_config.get("rotation", "1 day"),
        retention=log_config.get("retention", "30 days"),
        level=log_config.get("file_level", "DEBUG") if verbose else log_config.get("file_level", "INFO"),
        format=file_format,
        colorize=True,
        backtrace=True,
        diagnose=True
    )
    
    # Console logger
    logger.add(
        sys.stdout,
        level=log_config.get("console_level", "DEBUG") if verbose else log_config.get("console_level", "INFO"),
        format=console_format,
        colorize=True,
        backtrace=True,
        diagnose=True
    )

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Scrape football data from fbref.com")
    parser.add_argument("--league", "-l", help="League key to scrape (e.g. premier_league)")
    parser.add_argument("--url", "-u", help="Custom URL to scrape")
    parser.add_argument("--all", "-a", action="store_true", help="Scrape all leagues")
    parser.add_argument("--historical", action="store_true", help="Scrape historical data")
    parser.add_argument("--no-save", action="store_true", help="Don't save to CSV files")
    parser.add_argument("--config", "-c", default="config_url.yaml", help="Path to config file")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    return parser.parse_args()

def main():
    """Main function to run the scraper from command line."""
    args = parse_args()
    
    # Setup logger
    setup_logger(config_path=args.config, verbose=args.verbose)
    
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