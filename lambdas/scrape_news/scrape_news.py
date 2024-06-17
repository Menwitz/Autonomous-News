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

news_websites = [
    "https://www.sbnation.com/",
    "https://goal.com",
    "https://bleacherreport.com/",
    "https://www.espn.com/",
    "https://sports.yahoo.com/",
    "https://www.reuters.com/sports/",
    "https://www.foxsports.com/",
    "https://www.skysports.com/",
    "https://www.yardbarker.com/",
    "https://www.nbcsports.com/"
]

def fetch_headlines(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        if "sbnation.com" in url:
            headlines = soup.select('h2.c-entry-box--compact__title')
        elif "goal.com" in url:
            headlines = soup.select('h3.article-title')
        elif "bleacherreport.com" in url:
            headlines = soup.select('h3.atom-headline')
        elif "espn.com" in url:
            headlines = soup.select('h1.headline')
        elif "sports.yahoo.com" in url:
            headlines = soup.select('h3')
        elif "reuters.com" in url:
            headlines = soup.select('h3.story-title')
        elif "foxsports.com" in url:
            headlines = soup.select('h1.headline')
        elif "skysports.com" in url:
            headlines = soup.select('h1.news-list__headline')
        elif "yardbarker.com" in url:
            headlines = soup.select('h3')
        elif "nbcsports.com" in url:
            headlines = soup.select('h2.tease-card__headline')
        else:
            print(f"No specific parser for {url}")
            return []
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
