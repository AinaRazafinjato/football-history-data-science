# 🏆 Football History Data Science Project

A comprehensive data science project for analyzing football (soccer) match data across multiple leagues and seasons. This project combines web scraping, data processing, exploratory analysis, and predictive modeling to extract insights from historical football data.

## 🔍 Project Overview

This project aims to:
- 📊 Create a comprehensive database of football statistics from multiple leagues
- 🧹 Clean and standardize data for analysis
- 📈 Analyze performance trends of clubs and leagues
- 🔑 Identify key success factors in football performance
- 🔮 Build predictive models for match outcomes
- 📉 Visualize insights through notebooks and reports

## 📁 Project Structure

```
football_history/
├── .env                  # Environment variables
├── data/                 # Data storage
│   ├── raw/              # Raw data from web scraping
│   │   └── *.csv         # Raw league data files
│   ├── processed/        # Cleaned and standardized data
│   │   └── *-processed.csv # Processed league data files
│   └── results/          # Results from models and analyses
├── src/                  # Source code
│   ├── data/             # Data preprocessing functions
│   │   ├── logs/         # Log folder for data processing
│   │   │   └── *.log     # Log files for processing
│   │   ├── process_csv.py# Main data processing script
│   │   ├── config_csv.yaml# Configuration for processing
│   │   └── README.md     # Usage examples for processing
│   ├── scraping/         # Web scraping functionality
│   │   ├── logs/         # Log folder for scraping
│   │   │   └── *.log     # Log files for scraping
│   │   ├── scrapers.py   # WebScraper class for data collection
│   │   ├── main.py       # Script to run the scraper
│   │   ├── config_url.yaml# Configuration for scraping
│   │   └── README.md     # Usage examples for scraping
├── tests/                # Unit tests
│   ├── test_scraping.py
│   ├── test_preprocessing.py
│   └── test_models.py
├── .gitignore            # Git ignore file
├── LICENSE               # Project license
├── README.md             # Project overview and instructions
└── requirements.txt      # Project dependencies
```

## ⚙️ Installation

To set up the project:

```bash
# Clone the repository
git clone https://github.com/yourusername/football_history.git
cd football_history

# Create a virtual environment (optional but recommended)
python -m venv .env

# Activate the virtual environment
# On Windows
.env\Scripts\activate
# On macOS/Linux
source .env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## 🚀 Usage

### 🌐 Data Collection
The project uses web scraping to collect football match data from fbref.com. The main script is located in `src.scraping.main.py`.:

```bash
# Basic usage - scrape default league
python -m src.scraping.main

# Scrape a specific league
python -m src.scraping.main --league premier_league

# Scrape all configured leagues
python -m src.scraping.main --all

# Use a custom URL
python -m src.scraping.main --url "https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures"
```

### 🧮 Data Processing
Process raw CSV files into standardized formats:

```bash
# Process a specific file
python -m src.data.process_csv --csv "path/to/file.csv"

# Process all CSV files in the raw folder
python -m src.data.process_csv --all

# Run with verbose output
python -m src.data.process_csv --verbose
```

### 📊 Analysis
Run exploratory analysis using the Jupyter notebook:

- 🔬 Open `exploratory_analysis.ipynb` to explore data distributions, correlations, and trends.
- 📝 Evaluate predictive models: Open `model_evaluation.ipynb` to see model performance comparisons.

## ⚙️ Configuration
The project uses configuration files to control data processing:

- `config_url.yaml` - Controls web scraping behavior:
    - 🔗 League URLs
    - 📋 Data extraction rules
    - 📝 Logging settings
    - ⚠️ Error handling settings
- `config_csv.yaml` - Controls CSV processing behavior:
    - 📑 Column specifications
    - 🏢 Team name normalization
    - 📂 File paths and patterns
    - 🔄 Processing workflow
    - 📝 Logging settings


## 💻 Tech Stack
- **Data Collection**: 🕷️ Python web scraping with pandas
- **Data Processing**: 🐼 Pandas, 🔢 NumPy
- **Analysis**: 🧠 Scikit-learn, 📊 Matplotlib, 🌊 Seaborn
- **Testing**: 🔍 Unittest, ✅ pytest

## 🚧 Current Status
This project is in active development with ongoing work on data collection and preprocessing pipelines.

## 👥 Contributing
Contributions are welcome! Please submit pull requests or open issues for any suggestions.

## 📄 License
This project is licensed under the MIT License.