import unittest
from src.scraping.scrapers import WebScraper

class TestWebScraper(unittest.TestCase):

    def setUp(self):
        self.scraper = WebScraper()

    def test_fetch_data(self):
        url = "http://example.com"
        data = self.scraper.fetch_data(url)
        self.assertIsNotNone(data)
        self.assertIn("<html>", data)  # Basic check for HTML content

    def test_parse_data(self):
        raw_data = "<html><body><h1>Test</h1></body></html>"
        parsed_data = self.scraper.parse_data(raw_data)
        self.assertEqual(parsed_data, {"title": "Test"})  # Example expected output

if __name__ == '__main__':
    unittest.main()