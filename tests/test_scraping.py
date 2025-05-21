import sys
import os
import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from pathlib import Path

# Ajouter le chemin du module src au chemin de recherche Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock DATA_DIR avant d'importer WebScraper
with patch('src.scraping.config.DATA_DIR', Path('/mock/path')):
    from src.scraping.scrapers import WebScraper

class TestWebScraper(unittest.TestCase):
    
    def setUp(self):
        # URL de test
        self.test_url = "https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures"
        
        # Créer des données de test
        self.test_data = pd.DataFrame({
            'Date': ['2024-08-17', '2024-08-18', '2024-08-19'],
            'Home': ['Team A', 'Team B', 'Team C'],
            'Score': ['1-0', '2-2', '0-3'],
            'Away': ['Team D', 'Team E', 'Team F']
        })
        
        # Patcher DATA_DIR pour tous les tests
        self.data_dir_patcher = patch('src.scraping.scrapers.DATA_DIR', Path('/mock/path'))
        self.mock_data_dir = self.data_dir_patcher.start()

    def tearDown(self):
        # Arrêter le patcher après chaque test
        self.data_dir_patcher.stop()

    @patch('pandas.read_html')
    def test_parse_data(self, mock_read_html):
        # Configurer le mock pour renvoyer nos données de test
        mock_read_html.return_value = [self.test_data]
        
        # Créer une instance du scraper
        scraper = WebScraper(self.test_url)
        
        # Tester parse_data
        result = scraper.parse_data()
        
        # Vérifier que read_html a été appelé avec la bonne URL
        mock_read_html.assert_called_once_with(self.test_url)
        
        # Vérifier que le résultat est égal à nos données de test
        pd.testing.assert_frame_equal(result, self.test_data)
        pd.testing.assert_frame_equal(scraper.data, self.test_data)

    @patch('pandas.read_html')
    def test_save_to_csv_custom_filename(self, mock_read_html):
        # Configurer le mock
        mock_read_html.return_value = [self.test_data]
        
        # Créer un scraper et charger des données
        scraper = WebScraper(self.test_url)
        scraper.parse_data()
        
        # Mock DataFrame.to_csv pour éviter d'écrire un fichier réel
        with patch.object(pd.DataFrame, 'to_csv') as mock_to_csv:
            result = scraper.save_to_csv(filename="test_output.csv")
            
            # Vérifier que to_csv a été appelé avec le bon chemin
            expected_path = Path('/mock/path') / 'raw' / 'test_output.csv'
            mock_to_csv.assert_called_once_with(expected_path, index=False)
            self.assertTrue(result)

    @patch('pandas.read_html')
    def test_save_to_csv_auto_filename(self, mock_read_html):
        # Configurer le mock
        mock_read_html.return_value = [self.test_data]
        
        # Créer un scraper et charger des données
        scraper = WebScraper(self.test_url)
        scraper.parse_data()
        
        # Mock DataFrame.to_csv
        with patch.object(pd.DataFrame, 'to_csv') as mock_to_csv:
            result = scraper.save_to_csv()
            
            # Vérifier que to_csv a été appelé et que le chemin a la bonne structure
            mock_to_csv.assert_called_once()
            args = mock_to_csv.call_args[0]
            path_arg = str(args[0])  # Convertir Path en string pour les tests
            
            # Vérifier les éléments du chemin de façon indépendante du système d'exploitation
            mock_path = str(Path('/mock/path/raw'))
            self.assertTrue(mock_path.replace('/', '\\') in path_arg or mock_path in path_arg)
            self.assertIn('9', path_arg)
            self.assertIn('fixtures.csv', path_arg)
            self.assertTrue(result)

    def test_save_to_csv_no_data(self):
        # Créer un scraper sans charger de données
        scraper = WebScraper(self.test_url)
        
        # Vérifier qu'une exception est levée
        with self.assertRaises(Exception):
            scraper.save_to_csv()

if __name__ == '__main__':
    unittest.main()