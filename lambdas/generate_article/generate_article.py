import json
import boto3
import os
import openai
from datetime import datetime
from botocore.exceptions import ClientError
from typing import List, Dict
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')
headlines_table = dynamodb.Table('NewsHeadlines')
articles_table = dynamodb.Table('GeneratedArticles')

# Retrieve OpenAI API key from environment variables
openai.api_key = os.getenv('OPENAI_API_KEY')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def lambda_handler(event: dict, context: dict) -> dict:
    try:
        headlines = retrieve_headlines()
        for headline in headlines:
            headline_text = headline['headline']
            article = generate_article(headline_text)
            store_article(articles_table, headline_text, article)
        
        return {
            'statusCode': 200,
            'body': json.dumps('Articles generated and stored successfully')
        }
    except Exception as e:
        logger.error(f'Unhandled exception: {str(e)}')
        return {
            'statusCode': 500,
            'body': json.dumps(f'Unhandled exception: {str(e)}')
        }

def retrieve_headlines() -> List[Dict[str, str]]:
    try:
        response = headlines_table.scan()
        return response.get('Items', [])
    except ClientError as e:
        logger.error(f'Error retrieving headlines: {e.response["Error"]["Message"]}')
        raise RuntimeError(f'Error retrieving headlines: {e.response["Error"]["Message"]}')

def generate_article(headline: str) -> str:
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Write a detailed article based on the following headline: {headline}",
            max_tokens=500
        )
        return response.choices[0].text.strip()
    except Exception as e:
        logger.error(f'Error generating article: {str(e)}')
        raise RuntimeError(f'Error generating article: {str(e)}')

def store_article(table, headline: str, article: str) -> None:
    try:
        timestamp = datetime.utcnow().isoformat()
        url = f"https://example.com/{headline.replace(' ', '-').lower()}"
        table.put_item(
            Item={
                'url': url,
                'headline': headline,
                'article': article,
                'timestamp': timestamp
            }
        )
    except ClientError as e:
        logger.error(f'Error storing article: {e.response["Error"]["Message"]}')
        raise RuntimeError(f'Error storing article: {e.response["Error"]["Message"]}')
