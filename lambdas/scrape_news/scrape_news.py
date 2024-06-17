import json
import requests
from bs4 import BeautifulSoup
import boto3
from datetime import datetime
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from botocore.config import Config
from concurrent.futures import ThreadPoolExecutor, as_completed

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb', config=Config(retries={'max_attempts': 10, 'mode': 'standard'}))
table = dynamodb.Table('NewsHeadlines')

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

def fetch_headlines(url, selector):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        headlines = soup.select(selector)
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
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(fetch_headlines, url, selector): url for url, selector in news_websites.items()}
        for future in as_completed(futures):
            url = futures[future]
            try:
                headlines = future.result()
                for headline in headlines:
                    store_headline(url, headline)
            except Exception as e:
                print(f"Error processing {url}: {e}")

    return {
        'statusCode': 200,
        'body': json.dumps('Headlines scraped successfully')
    }

if __name__ == "__main__":
    # For local testing
    scrape_news(None, None)
