import unittest
from scraper import is_valid_url, fetch_headlines
from config import news_websites

class TestScrapingFunction(unittest.TestCase):
    def test_valid_url(self):
        self.assertTrue(is_valid_url("https://www.example.com"))
        self.assertFalse(is_valid_url("invalid-url"))
    
    def test_fetch_headlines(self):
        headlines = fetch_headlines("https://www.sbnation.com/", 'h2.c-entry-box--compact__title')
        self.assertIsInstance(headlines, list)

if __name__ == '__main__':
    unittest.main()
