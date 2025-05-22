# Script Usage Examples

### 🧮 Data Processing
Process raw CSV files into standardized formats:

```bash
# Process a specific file
python -m process_csv --csv "path/to/file.csv"

# Process all CSV files in the raw folder
python -m process_csv --all

# Run with verbose output
python -m process_csv --verbose
```

The script supports various options through command-line arguments and loads configurations from YAML files for flexible data processing.