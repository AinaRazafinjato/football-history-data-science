"""
Football Web Scraper
====================

A module for scraping football match data from FBref.com and saving it as CSV files.

This module provides tools to fetch league schedule data, parse it, and save it
in a structured format for further analysis.

Usage:
    from football_history.src.scraping import WebScraper
    
    # Create a scraper instance with a FBref URL
    scraper = WebScraper("https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures")
    
    # Parse the data
    df = scraper.parse_data()
    
    # Save data to CSV
    scraper.save_to_csv()
"""

import pandas as pd
from pathlib import Path
from loguru import logger
from typing import Optional
import os


# Get the project root directory (parent of src)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Define the data directory
DATA_DIR = os.path.join(BASE_DIR, 'data')


class WebScraper:
    """
    A web scraper for football data from FBref.com
    
    This class handles fetching, parsing and saving tabular data from FBref.com,
    particularly focused on league schedules and match results.
    
    Attributes:
        url (str): The URL to scrape data from
        data (pd.DataFrame): The scraped data after parsing
    
    Example URLs:
        - Current season: https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures
        - Past season: https://fbref.com/en/comps/9/2023-2024/schedule/2023-2024-Premier-League-Scores-and-Fixtures
    """
    
    def __init__(self, url: str):
        """
        Initialize the WebScraper with a target URL.
        
        Args:
            url (str): The FBref URL to scrape data from
        """
        self.url = url
        self.data = None

    def parse_data(self) -> pd.DataFrame:
        """
        Parse the HTML table data from the specified URL.
        
        Returns:
            pd.DataFrame: The parsed table data
            
        Raises:
            Exception: If no tables are found or parsing fails
        """
        try:
            # Parse the HTML tables into DataFrames
            tables = pd.read_html(self.url)
            if tables:
                # Store the first table found
                self.data = tables[0]
                logger.info(f"Successfully parsed table with {len(self.data)} rows")
                return self.data
            else:
                logger.error("No tables found in the webpage")
                raise Exception("No tables found in the webpage")
        except Exception as e:
            logger.error(f"Error parsing HTML table: {str(e)}")
            raise Exception(f"Error parsing HTML table: {str(e)}")
    
    def generate_csv_filename(self, df: pd.DataFrame) -> str:
        """
        Generate a CSV filename based on the URL and season extracted from the DataFrame.
        
        The filename format is: {league-name}-{start_year}-{end_year}.csv
        
        Args:
            df (pd.DataFrame): The DataFrame containing match data with a 'Date' column
            
        Returns:
            str: The generated CSV filename
            
        Raises:
            ValueError: If the 'Date' column is missing or contains no valid dates
        """
        logger.info("Generating CSV filename")
        
        # Check for Date column
        if 'Date' not in df.columns:
            logger.error("'Date' column not found in DataFrame")
            raise ValueError("'Date' column missing in DataFrame")
            
        # Convert Date column to datetime
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        if df['Date'].dropna().empty:
            logger.error("No valid dates found in DataFrame")
            raise ValueError("No valid dates found in DataFrame")
        
        # Extract season years
        start_year = df['Date'].min().year
        end_year = df['Date'].max().year
        season = f"{start_year}-{end_year}"
        logger.info(f"Season identified: {season}")
        
        # Extract league name
        league_name = self.extract_league_name(self.url)
        filename = f"{league_name}-{season}.csv"
        logger.info(f"Generated filename: {filename}")
        
        return filename

    def extract_league_name(self, url: str) -> str:
        """
        Extract the league name from the FBref URL.
        
        Args:
            url (str): The FBref URL
            
        Returns:
            str: The extracted league name
        """
        try:
            # Parse the URL to get relevant parts
            url_parts = url.split('/')
            
            # Extract the league name from the URL structure
            # For URLs like: .../comps/9/schedule/Premier-League-Scores-and-Fixtures
            # Or URLs like: .../comps/9/2023-2024/schedule/2023-2024-Premier-League-Scores-and-Fixtures
            if 'schedule' in url_parts:
                schedule_index = url_parts.index('schedule')
                if schedule_index + 1 < len(url_parts):
                    name_part = url_parts[schedule_index + 1]
                    
                    # Remove any season years from the beginning of the name
                    if '-' in name_part:
                        # Check for patterns like "2023-2024-Premier-League-Scores-and-Fixtures"
                        parts = name_part.split('-')
                        if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
                            name_part = '-'.join(parts[2:])  # Skip the "2023-2024" part
                    
                    # Split by dash and remove common words
                    elements = name_part.split('-')
                    exclude = {"Scores", "and", "Fixtures"}
                    league_parts = [el for el in elements if el not in exclude]
                    league_name = "-".join(league_parts)
                    
                    logger.debug(f"Extracted league name: {league_name}")
                    return league_name
            
            # Fallback to old behavior
            last_part = url.split('/')[-1]
            elements = last_part.split('-')
            exclude = {"Scores", "and", "Fixtures"}
            league_parts = [el for el in elements if el not in exclude]
            league_name = "-".join(league_parts)
            logger.debug(f"Extracted league name: {league_name}")
            return league_name
        except Exception as e:
            logger.error(f"Error extracting league name: {e}")
            return "unknown-league"

    def save_to_csv(self, filename: Optional[str] = None) -> bool:
        """
        Save the scraped data to a CSV file.
        
        Args:
            filename (str, optional): Custom filename for the CSV.
                                     If None, one will be generated.
        
        Returns:
            bool: True if saving was successful
            
        Raises:
            ValueError: If there is no data to save
            IOError: If there's an error saving the file
        """
        if self.data is None:
            logger.error("No data available to save")
            raise ValueError("No data to save. Call parse_data() first.")
        
        # Generate filename if not provided
        if filename is None:
            filename = self.generate_csv_filename(self.data)
            
        # Create full path
        csv_path = Path(DATA_DIR) / "raw" / filename
        logger.info(f"Saving data to {csv_path}")
        
        try:
            # Create directory if it doesn't exist
            csv_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save the DataFrame to a CSV file
            self.data.to_csv(csv_path, index=False)
            logger.success(f"Data successfully saved to {csv_path}")
            return True
        except Exception as e:
            logger.error(f"Error saving data: {e}")
            raise IOError(f"Error saving data: {e}")


def scrape_league(url: str, save: bool = True) -> pd.DataFrame:
    """
    Convenience function to scrape a league schedule and optionally save it.
    
    Args:
        url (str): FBref URL for the league
        save (bool, optional): Whether to save the data as CSV. Defaults to True.
        
    Returns:
        pd.DataFrame: The scraped league data
        
    Example:
        >>> df = scrape_league("https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures")
    """
    scraper = WebScraper(url)
    data = scraper.parse_data()
    
    if save:
        scraper.save_to_csv()
        
    return data