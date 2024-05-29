import json
import requests
from bs4 import BeautifulSoup
import boto3
from datetime import datetime
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from botocore.config import Config

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('NewsHeadlines')

# List of news websites
news_websites = [
    "https://example1.com",
    "https://example2.com",
    # Add all 100 news websites here
]

def fetch_headlines(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        # This part may need customization for each site
        headlines = soup.find_all('h1')  # Example: Change based on the site's structure
        return [headline.get_text(strip=True) for headline in headlines]
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []

def store_headline(url, headline):
    try:
        table.put_item(
            Item={
                'url': url,
                'headline': headline,
                'timestamp': datetime.utcnow().isoformat()
            }
        )
    except (NoCredentialsError, PartialCredentialsError) as e:
        print(f"Credentials error: {e}")
    except Exception as e:
        print(f"Error storing headline: {e}")

def scrape_news(event, context):
    for url in news_websites:
        headlines = fetch_headlines(url)
        for headline in headlines:
            store_headline(url, headline)
    return {
        'statusCode': 200,
        'body': json.dumps('Headlines scraped successfully')
    }

if __name__ == "__main__":
    # For local testing
    scrape_news(None, None)
