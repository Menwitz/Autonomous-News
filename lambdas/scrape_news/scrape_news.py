import json
import os
import requests
from bs4 import BeautifulSoup
import boto3
from datetime import datetime
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from botocore.config import Config
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Environment Variables
table_name = os.getenv('DYNAMODB_TABLE', 'NewsHeadlines')
timeout = int(os.getenv('REQUEST_TIMEOUT', 10))

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb', config=Config(retries={'max_attempts': 10, 'mode': 'standard'}))
table = dynamodb.Table(table_name)

# Logger setup
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# News websites and their headline selectors
news_websites = {
    "https://www.sbnation.com/": 'h2.c-entry-box--compact__title',
    "https://goal.com": 'h3.article-title',
    "https://bleacherreport.com/": 'h3.atom-headline',
    "https://www.espn.com/": 'h1.headline',
    "https://sports.yahoo.com/": 'h3',
    "https://www.reuters.com/sports/": 'h3.story-title',
    "https://www.foxsports.com/": 'h1.headline',
    "https://www.skysports.com/": 'h1.news-list__headline',
    "https://www.yardbarker.com/": 'h3',
    "https://www.nbcsports.com/": 'h2.tease-card__headline'
}

# Request session with retry logic
session = requests.Session()
headers = {'User-Agent': 'Mozilla/5.0'}
retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    method_whitelist=["HEAD", "GET", "OPTIONS"]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("https://", adapter)
session.mount("http://", adapter)

# Documentation and Comments
"""
Lambda function to scrape headlines from news websites and store them in DynamoDB.

Environment Variables:
- DYNAMODB_TABLE: NewsHeadLines.
- REQUEST_TIMEOUT: Timeout for HTTP requests.
"""

def log_error(message):
    """Logs errors to AWS CloudWatch"""
    logger.error(message)

def fetch_headlines(url, selector):
    """
    Fetches headlines from a given URL using the specified CSS selector.

    Args:
    - url (str): The URL of the news website.
    - selector (str): The CSS selector for extracting headlines.

    Returns:
    - list: A list of extracted headlines.
    """
    try:
        response = session.get(url, timeout=timeout, verify=False if "nbc" in url else True, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        headlines = soup.select(selector)
        return [headline.get_text(strip=True) for headline in headlines]
    except requests.RequestException as e:
        log_error(f"Error fetching {url}: {e}")
        return []

def store_headline(url, headline):
    """
    Stores a single headline in DynamoDB.

    Args:
    - url (str): The URL of the news website.
    - headline (str): The headline text.
    """
    try:
        table.put_item(
            Item={
                'url': url,
                'headline': headline,
                'timestamp': datetime.utcnow().isoformat()
            }
        )
    except (NoCredentialsError, PartialCredentialsError) as e:
        log_error(f"Credentials error: {e}")
    except Exception as e:
        log_error(f"Error storing headline: {e}")

def batch_store_headlines(headlines):
    """
    Stores multiple headlines in DynamoDB using batch operations.

    Args:
    - headlines (list): A list of dictionaries containing headline data.
    """
    try:
        with table.batch_writer() as batch:
            for item in headlines:
                batch.put_item(Item=item)
    except Exception as e:
        log_error(f"Error batch storing headlines: {e}")

def scrape_news(event, context):
    """
    Lambda handler function to scrape headlines from configured news websites.

    Args:
    - event (dict): Lambda event data.
    - context (object): Lambda context object.

    Returns:
    - dict: Response status and message.
    """
    headlines_data = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(fetch_headlines, url, selector): url for url, selector in news_websites.items()}
        for future in as_completed(futures):
            url = futures[future]
            try:
                headlines = future.result()
                for headline in headlines:
                    headlines_data.append({'url': url, 'headline': headline, 'timestamp': datetime.now(datetime.UTC).isoformat()})
            except Exception as e:
                log_error(f"Error processing {url}: {e}")
    batch_store_headlines(headlines_data)

    return {
        'statusCode': 200,
        'body': json.dumps('Headlines scraped successfully')
    }

if __name__ == "__main__":
    # For local testing
    scrape_news(None, None)
