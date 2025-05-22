# Process CSV - Documentation

A Python script for automated processing of football data from CSV files.

## Description

This script allows you to:
- Load football match data from CSV files
- Clean and transform data (normalize team names, convert scores, etc.)
- Save processed data in a standardized format
- Process multiple files in a single command

## Installation

```bash
# Install dependencies
pip install pandas loguru pyyaml
```

## Project Structure

```
football_history/
├── data/
│   ├── raw/          # Raw data (.csv)
│   └── processed/    # Cleaned data
└── src/
    └── data/
        ├── process_csv.py    # Main script
        ├── config_csv.yaml   # Configuration
        └── logs/             # Execution logs
```

## Configuration

The `config_csv.yaml` file controls the script behavior:

```yaml
columns:
  rows_to_drop: [...]        # Columns required to keep a row
  columns_to_drop: [...]     # Columns to remove
  required_columns: [...]    # Mandatory columns
  cols_to_convert_int: [...]  # Columns to convert to integers
  cols_to_convert_float: [...] # Columns to convert to decimals
  cols_order: [...]          # Final column order

team_name_corrections:       # Team name normalization
  Utd: "United"
  # etc...

paths:
  raw_dir: "raw"             # Raw data folder
  processed_dir: "processed" # Processed data folder
  logs_dir: "logs"           # Logs folder

files:
  default_csv: "raw/Premier-League-2024-2025.csv"  # Default file
  process_all: true          # Process all files
  file_pattern: "*.csv"      # Pattern for files to process
```

## Usage

### Process a specific file
```bash
python -m process_csv --csv "path/to/file.csv"
```

### Process all CSV files in the raw folder
```bash
# Option 1: Via command line argument
python -m process_csv --all

# Option 2: By modifying config_csv.yaml (process_all: true)
python -m process_csv
```

### Additional options
```bash
python -m process_csv --verbose  # Verbose mode (more details)
python -m process_csv --config "other_config.yaml"  # Use another configuration
```

## How it works

1. **Data loading**: The script loads the specified CSV files
2. **Cleaning**:
   - Removes rows with missing data in key columns
   - Removes unnecessary columns
   - Splits score column into score_home and score_away
   - Converts xG into separate columns
3. **Transformation**:
   - Normalizes team names
   - Converts columns to appropriate types
   - Reorders columns according to defined order
4. **Saving**: Saves the result in the processed folder with a standardized name

## Logging

The script generates detailed logs:
- In the console (colored)
- In daily files in the logs/ folder

### Sample output
```
2025-05-22 15:49:35 | INFO     | Starting process_csv.py script
2025-05-22 15:49:35 | INFO     | Data folder: .../football_history/data
2025-05-22 15:49:35 | INFO     | Raw folder: .../football_history/data/raw
2025-05-22 15:49:35 | INFO     | Found 3 CSV files to process
2025-05-22 15:49:36 | SUCCESS  | 3/3 files successfully processed
```