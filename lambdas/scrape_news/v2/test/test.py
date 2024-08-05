import sys
import os

# Add the parent directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from scraper import is_valid_url, fetch_headlines
import config
from config import news_websites
import json
import urllib

class TestScrapingFunction(unittest.TestCase):
    def test_valid_url(self):
        self.assertTrue(is_valid_url("https://www.example.com"))
        self.assertFalse(is_valid_url("invalid-url"))
    
    def test_fetch_headlines(self):
        for url, selector in news_websites.items():
            headlines = fetch_headlines(url, selector)
            self.assertIsInstance(headlines, list)
            # grep site name from the url
            parsed_url = urllib.parse.urlparse(url)
            site_name = parsed_url.netloc.split('.')[1]
            # Log the results to an output file
            with open("results/" + site_name + ".json", 'w') as file:
                json.dump(headlines, file, indent=4)

            print("TU logged to results/" + site_name + ".json")

if __name__ == '__main__':
    unittest.main()
