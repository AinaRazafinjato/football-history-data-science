# Script Usage Examples

### 🌐 Data Collection
The project uses web scraping to collect football match data from fbref.com. The main script is located in `main.py`.:

```bash
# Basic usage - scrape default league
python -m main

# Scrape a specific league
python -m main --league premier_league

# Scrape all configured leagues
python -m main --all

# Use a custom URL
python -m main --url "https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures"
```

### 📜 Additional Options

```bash
# Retrieve historical data (if enabled in config)
python -m main --historical

# Just fetch data without saving (testing mode)
python -m main --all --no-save
```

The script supports various options through command-line arguments and loads configurations from YAML files for flexible data collecting.