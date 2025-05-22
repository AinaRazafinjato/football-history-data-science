import os
import sys
import yaml
import argparse
import pandas as pd
from pathlib import Path
from loguru import logger

# Define default configuration for fallback
DEFAULT_CONFIG = {
    "columns": {
        "rows_to_drop": ["Date", "Home", "Away", "Venue"],
        "columns_to_drop": ["Day", "Match Report", "Notes", "Venue", "Attendance", "Referee"],
        "required_columns": ["Score", "Wk"],
        "cols_to_convert_int": ["Wk", "Score_Home", "Score_Away"],
        "cols_to_convert_float": ["xG_Home", "xG_Away"],
        "cols_order": ["Wk", "Date", "Time", "Home", "xG_Home", "Score_Home", 
                      "Score_Away", "xG_Away", "Away"]
    },
    "team_name_corrections": {
        "Utd": "United", "Nott'ham": "Nottingham", "Wolves": "Wolverhampton Wanderers",
        "Brighton": "Brighton & Hove Albion", "Tottenham": "Tottenham Hotspur",
        "West Ham": "West Ham United", "FC": "", "AFC": "", "Man": "Manchester",
        "Spurs": "Tottenham Hotspur"
    },
    "paths": {
        "raw_dir": "raw",
        "processed_dir": "processed",
        "logs_dir": "logs"
    },
    "files": {
        "default_csv": "raw/Premier-League-2024-2025.csv",
        "process_all": True,
        "file_pattern": "*.csv"
    }
}

# Global variables that will be initialized when needed
CONFIG = None
ROWS_TO_DROP = None
COLUMNS_TO_DROP = None
REQUIRED_COLUMNS = None
COLS_TO_CONVERT_INT = None
COLS_TO_CONVERT_FLOAT = None
COLS_ORDER = None
TEAM_NAME_CORRECTIONS = None
BASE_DIR = None
DATA_DIR = None
RAW_DIR = None
PROCESSED_DIR = None
LOG_DIR = None

def init_config(config_path="config_csv.yaml"):
    """
    Initialize the configuration and global variables.
    
    Args:
        config_path (str): Path to the configuration file
        
    Returns:
        dict: The loaded configuration
    """
    global CONFIG, ROWS_TO_DROP, COLUMNS_TO_DROP, REQUIRED_COLUMNS
    global COLS_TO_CONVERT_INT, COLS_TO_CONVERT_FLOAT, COLS_ORDER, TEAM_NAME_CORRECTIONS
    global BASE_DIR, DATA_DIR, RAW_DIR, PROCESSED_DIR, LOG_DIR
    
    # Load configuration
    CONFIG = load_config(config_path)
    
    # Extract constants from configuration
    ROWS_TO_DROP = CONFIG["columns"]["rows_to_drop"]
    COLUMNS_TO_DROP = CONFIG["columns"]["columns_to_drop"]
    REQUIRED_COLUMNS = CONFIG["columns"]["required_columns"]
    COLS_TO_CONVERT_INT = CONFIG["columns"]["cols_to_convert_int"]
    COLS_TO_CONVERT_FLOAT = CONFIG["columns"]["cols_to_convert_float"]
    COLS_ORDER = CONFIG["columns"]["cols_order"]
    TEAM_NAME_CORRECTIONS = CONFIG["team_name_corrections"]
    
    # Define base directory and file directories
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    
    # Convert string paths to Path objects
    RAW_DIR = Path(os.path.join(DATA_DIR, CONFIG["paths"]["raw_dir"]))
    PROCESSED_DIR = Path(os.path.join(DATA_DIR, CONFIG["paths"]["processed_dir"]))
    LOG_DIR = Path(os.path.join(os.path.dirname(os.path.abspath(__file__)), CONFIG["paths"]["logs_dir"]))
    
    # Create directories if they don't exist
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    
    return CONFIG

def setup_logger(verbose=False):
    """
    Configure the logger based on settings.
    
    Args:
        verbose (bool): Whether to enable verbose logging
    """
    global LOG_DIR
    
    # Ensure LOG_DIR is initialized
    if LOG_DIR is None:
        init_config()
    
    # Remove default configuration
    logger.remove()
    
    # Format with colors for terminal
    CONSOLE_FORMAT = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>"
    
    # Format with color markers for log file
    FILE_FORMAT = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>"
    
    # File logger - with markup to preserve color information
    logger.add(
        os.path.join(LOG_DIR, "process_csv_{time:YYYY-MM-DD}.log"),
        rotation="1 day",
        retention="30 days",
        level="DEBUG" if verbose else "INFO",
        format=FILE_FORMAT,
        colorize=True,
        backtrace=True,
        diagnose=True
    )
    
    # Console logger - with colors enabled
    logger.add(
        sys.stdout,
        level="DEBUG" if verbose else "INFO",
        format=CONSOLE_FORMAT,
        colorize=True,
        backtrace=True,
        diagnose=True
    )

def load_config(config_path="config_csv.yaml"):
    """
    Charge la configuration depuis un fichier YAML.
    
    Args:
        config_path (str): Chemin vers le fichier de configuration.
        
    Returns:
        dict: Configuration chargée.
    """
    try:
        # Get the directory of the current script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # If config_path is not absolute, make it relative to current_dir
        if not os.path.isabs(config_path):
            config_path = os.path.join(current_dir, config_path)
            
        logger.info(f"Loading configuration from: {config_path}")
        
        if not os.path.exists(config_path):
            logger.warning(f"Configuration file not found: {config_path}, using default configuration")
            return DEFAULT_CONFIG
            
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
            logger.info(f"Configuration chargée depuis {config_path}")
            return config
    except Exception as e:
        logger.error(f"Erreur lors du chargement de la configuration: {e}, using default configuration")
        return DEFAULT_CONFIG

def parse_arguments():
    """
    Parse command line arguments.
    
    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(description="Transformer les données de football depuis un fichier CSV")
    parser.add_argument("--csv", help="Chemin vers le fichier CSV à traiter")
    parser.add_argument("--config", default="config_csv.yaml", help="Chemin vers le fichier de configuration")
    parser.add_argument("--verbose", action="store_true", help="Mode verbeux")
    parser.add_argument("--all", action="store_true", help="Traiter tous les fichiers CSV dans le dossier raw")
    return parser.parse_args()

def load_csv_data(csv_path):
    """
    Charge les données depuis un fichier CSV.

    Args:
        csv_path (str): Chemin vers le fichier CSV.

    Returns:
        pd.DataFrame: Le DataFrame chargé depuis le CSV.
    """
    global RAW_DIR
    
    # Make sure RAW_DIR is initialized
    if RAW_DIR is None:
        init_config()
    
    try:
        # Ensure we're using absolute path
        if not os.path.isabs(csv_path):
            if os.path.exists(csv_path):
                abs_path = os.path.abspath(csv_path)
            else:
                # Try to resolve relative to RAW_DIR
                abs_path = os.path.join(RAW_DIR, os.path.basename(csv_path))
        else:
            abs_path = csv_path
            
        logger.info(f"Chargement des données depuis le fichier: {abs_path}")
        
        if not os.path.exists(abs_path):
            raise FileNotFoundError(f"Le fichier {abs_path} n'existe pas")
            
        df = pd.read_csv(abs_path)
        logger.success(f"Données chargées avec succès. Dimensions: {df.shape}")
        return df
    except Exception as e:
        logger.error(f"Erreur lors du chargement du fichier CSV: {e}")
        raise ValueError(f"Erreur lors du chargement du fichier CSV : {e}")


def clean_and_transform_data(df):
    """
    Nettoie et transforme les données chargées.

    Args:
        df (pd.DataFrame): Le DataFrame brut contenant les données.

    Returns:
        pd.DataFrame: Le DataFrame nettoyé et transformé.
    """
    # Make sure config is initialized
    if ROWS_TO_DROP is None:
        init_config()
    
    logger.info("Début du nettoyage et de la transformation des données")
    
    # Supprimer les lignes avec des valeurs manquantes dans les colonnes clés
    # But only check columns that actually exist in the dataframe
    initial_rows = len(df)
    existing_drop_cols = [col for col in ROWS_TO_DROP if col in df.columns]
    if existing_drop_cols:
        df = df.dropna(subset=existing_drop_cols)
        logger.info(f"{initial_rows - len(df)} lignes supprimées pour données manquantes")
    else:
        logger.warning("Aucune colonne à utiliser pour supprimer les lignes avec valeurs manquantes")
    
    # Supprimer les colonnes inutiles (une seule fois)
    columns_to_drop_existing = [col for col in COLUMNS_TO_DROP if col in df.columns]
    df = df.drop(columns=columns_to_drop_existing, errors='ignore')
    logger.info(f"Colonnes supprimées: {', '.join(columns_to_drop_existing)}")

    # Vérifier que toutes les colonnes obligatoires sont présentes
    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            logger.error(f"Colonne obligatoire manquante: {col}")
            raise ValueError(f"Colonne obligatoire manquante : {col}")
        
    # Renommer les colonnes xG et xG.1 en xG_Home et xG_Away avant de les supprimer
    if 'xG' in df.columns:
        df['xG_Home'] = df['xG']
    if 'xG.1' in df.columns:
        df['xG_Away'] = df['xG.1']

    # Convertir les colonnes de xG en valeurs numériques, les erreurs deviennent NaN
    if 'xG_Home' in df.columns:
        df['xG_Home'] = pd.to_numeric(df['xG_Home'], errors='coerce')
    if 'xG_Away' in df.columns:
        df['xG_Away'] = pd.to_numeric(df['xG_Away'], errors='coerce')

    # Diviser la colonne 'Score' en deux colonnes : 'Score_Home' et 'Score_Away'
    if 'Score' in df.columns:
        df[['Score_Home', 'Score_Away']] = df['Score'].str.split('–', expand=True)
        logger.info("Colonne 'Score' divisée en 'Score_Home' et 'Score_Away'")

        # Convertir les colonnes de score en valeurs numériques, les erreurs deviennent NaN
        df['Score_Home'] = pd.to_numeric(df['Score_Home'], errors='coerce')
        df['Score_Away'] = pd.to_numeric(df['Score_Away'], errors='coerce')

        # Supprimer la colonne originale 'Score'
        df = df.drop('Score', axis=1)
    
    # Supprimer les colonnes originales xG et xG.1 si elles existent encore
    columns_to_drop = [col for col in ["xG", "xG.1"] if col in df.columns]
    if columns_to_drop:
        df = df.drop(columns=columns_to_drop, axis=1)

    # Vérifier que toutes les colonnes nécessaires sont présentes pour la réorganisation
    missing_cols = [col for col in COLS_ORDER if col not in df.columns]
    if missing_cols:
        logger.warning(f"Colonnes manquantes pour la réorganisation: {missing_cols}")
        # Ajouter les colonnes manquantes avec des valeurs NULL
        for col in missing_cols:
            df[col] = None

    # Normaliser les noms des équipes dans les colonnes 'Home' et 'Away'
    if 'Home' in df.columns:
        df['Home'] = df['Home'].apply(normalize_team_name)
    if 'Away' in df.columns:
        df['Away'] = df['Away'].apply(normalize_team_name)
    logger.info("Noms d'équipes normalisés")

    # Convertir les colonnes spécifiques en entiers si possible, sinon garder None
    for col in COLS_TO_CONVERT_INT:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')
        else:
            logger.warning(f"Colonne {col} non trouvée pour la conversion en entier")

    # Convertir les colonnes spécifiques en float si possible, sinon garder None
    for col in COLS_TO_CONVERT_FLOAT:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').astype('float64')
        else:
            logger.warning(f"Colonne {col} non trouvée pour la conversion en float")
    
    # Réorganiser les colonnes dans l'ordre souhaité (seulement celles qui existent)
    available_cols = [col for col in COLS_ORDER if col in df.columns]
    df = df[available_cols]
    logger.info(f"Colonnes réorganisées dans l'ordre: {', '.join(available_cols)}")
    
    logger.success(f"Données nettoyées avec succès. Dimensions finales: {df.shape}")
    return df

def normalize_team_name(team_name):
    """
    Normalise les noms d'équipes en remplaçant les abréviations et corrections définies.
    
    Args:
        team_name (str): Le nom brut de l'équipe.
    
    Returns:
        str: Le nom normalisé de l'équipe.
    """
    # Make sure config is initialized
    if TEAM_NAME_CORRECTIONS is None:
        init_config()
    
    if not isinstance(team_name, str):
        return str(team_name)
    
    # Handle special cases for full team names
    if team_name == "Tottenham Spurs":
        return "Tottenham Hotspur"
    
    # Process individual words
    words = team_name.split()
    normalized_words = []
    
    for word in words:
        # Replace word if it has a correction
        replacement = TEAM_NAME_CORRECTIONS.get(word, word)
        normalized_words.append(replacement)
    
    # Filter out empty strings and join with spaces
    return " ".join(filter(None, normalized_words))


def generate_output_filename(csv_path, df):
    """
    Génère un nom de fichier pour la sortie basé sur le fichier d'entrée.

    Args:
        csv_path (str): Chemin du fichier CSV d'entrée.
        df (pd.DataFrame): Le DataFrame contenant les données.

    Returns:
        str: Le nom du fichier CSV de sortie.
    """
    logger.info("Génération du nom de fichier de sortie")
    
    # Obtenir le nom de base du fichier sans extension
    base_filename = Path(csv_path).stem

    # Obtenir le nom de sortie basé sur le nom de base
    try:
        output_filename = f"{base_filename}-processed.csv"
    except ValueError:
        logger.warning("Erreur lors de l'extraction de la saison, utilisation du nom de base par défaut")
    
    logger.info(f"Nom de fichier de sortie généré: {output_filename}")
    return output_filename


def save_to_csv(df, filename):
    """
    Sauvegarde le DataFrame dans un fichier CSV.

    Args:
        df (pd.DataFrame): Le DataFrame à sauvegarder.
        filename (str): Le nom du fichier CSV.
    """
    global PROCESSED_DIR
    
    # Make sure PROCESSED_DIR is initialized
    if PROCESSED_DIR is None:
        init_config()
    
    csv_path = PROCESSED_DIR / filename
    logger.info(f"Sauvegarde des données dans {csv_path}")
    try:
        df.to_csv(csv_path, index=False)
        logger.success(f"Données sauvegardées avec succès dans {csv_path}")
    except Exception as e:
        logger.error(f"Erreur lors de la sauvegarde des données: {e}")
        raise IOError(f"Erreur lors de la sauvegarde des données: {e}")


def process_csv_data(csv_path):
    """
    Traite les données à partir d'un fichier CSV et les sauvegarde dans un nouveau fichier.

    Args:
        csv_path (str): Chemin vers le fichier CSV contenant les données.

    Returns:
        pd.DataFrame: Le DataFrame traité.
    """
    logger.info(f"Début du traitement des données pour le fichier: {csv_path}")
    
    # Récupérer et nettoyer les données
    raw_data = load_csv_data(csv_path)
    cleaned_data = clean_and_transform_data(raw_data)
    
    # Générer le nom du fichier CSV et sauvegarder les données
    output_filename = generate_output_filename(csv_path, cleaned_data)
    save_to_csv(cleaned_data, output_filename)
    
    logger.success(f"Traitement terminé pour {csv_path}")
    return cleaned_data

def process_all_csv_files():
    """
    Traite tous les fichiers CSV présents dans le répertoire RAW_DIR.
    
    Returns:
        int: Nombre de fichiers traités avec succès
    """
    global CONFIG, RAW_DIR
    
    # Make sure config is initialized
    if CONFIG is None:
        init_config()
    
    logger.info(f"Recherche des fichiers CSV dans {RAW_DIR}")
    
    # Chercher tous les fichiers CSV dans le dossier raw
    pattern = CONFIG.get("files", {}).get("file_pattern", "*.csv")
    csv_files = list(RAW_DIR.glob(pattern))
    
    if not csv_files:
        logger.warning(f"Aucun fichier CSV trouvé dans {RAW_DIR}")
        return 0
    
    logger.info(f"Trouvé {len(csv_files)} fichiers CSV à traiter")
    
    # Traiter chaque fichier
    success_count = 0
    for csv_file in csv_files:
        try:
            logger.info(f"Traitement du fichier {csv_file.name}")
            process_csv_data(csv_file)
            success_count += 1
        except Exception as e:
            logger.error(f"Erreur lors du traitement de {csv_file.name}: {e}")
            continue
    
    logger.success(f"{success_count}/{len(csv_files)} fichiers traités avec succès")
    return success_count

def main():
    """Main function to run the script from command line."""
    try:
        # Parse command line arguments
        args = parse_arguments()
        
        # Initialize configuration and global variables
        init_config(args.config)
        
        # Setup logging
        setup_logger(args.verbose)
        
        logger.info("Démarrage du script process_csv.py")
        logger.info(f"Dossier de données: {DATA_DIR}")
        logger.info(f"Dossier raw: {RAW_DIR}")
        logger.info(f"Dossier processed: {PROCESSED_DIR}")
        
        # Determine if we should process all files
        process_all = args.all or CONFIG.get("files", {}).get("process_all", False)
        
        if process_all:
            # Process all CSV files in the raw directory
            files_processed = process_all_csv_files()
            if files_processed > 0:
                logger.success(f"Traitement par lot terminé. {files_processed} fichiers traités.")
            else:
                logger.warning("Aucun fichier n'a été traité.")
        else:
            # Process a single specified file
            default_csv_path = os.path.join(RAW_DIR, os.path.basename(CONFIG["files"]["default_csv"]))
            csv_path = args.csv if args.csv else default_csv_path
            df = process_csv_data(csv_path)
            logger.success("Les données ont été traitées et sauvegardées avec succès.")
            
        return 0
        
    except Exception as e:
        logger.error(f"Une erreur s'est produite: {e}")
        print(f"Une erreur s'est produite : {e}")
        return 1

# Only execute when run as a script, not when imported
if __name__ == "__main__":
    sys.exit(main())